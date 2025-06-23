import requests
import pandas as pd
from urllib.parse import quote_plus
import json
import time
from datetime import datetime, timezone, timedelta
import random


 # Load the CSV
df = pd.read_csv("./borough_postcodes.csv")  # Replace with your actual filename

# Convert to dictionary format
boroughs = {
    row["borough"]: row["postcodes"].split(";")
    for _, row in df.iterrows()
}

print("boroughs = " + json.dumps(boroughs, indent=4))  
#define variables, could add others for maxPrice etc


# define our user headers
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}
page_size = 24
max_pages_per_postcode = 42  # Assuming max pages per postcode
pages_per_postcode_to_sample = 25  # Number of random pages to scrape per postcode
SLEEP_TIME = 1    # Seconds to sleep between requests (avoid IP ban)
# Extract only required fields




def extract_minimal_fields(prop):
    return {
        "id": prop.get("id"),
        "date_listed": prop.get("firstVisibleDate"),
        "bedrooms": prop.get("bedrooms"),
        "bathrooms": prop.get("bathrooms"),
        "summary": prop.get("summary"),
        "address": prop.get("displayAddress"),
        "property_type": prop.get("propertySubType"),
        "price_amount": prop.get("price", {}).get("amount"),
        "price_frequency": prop.get("price", {}).get("frequency"),
        "latitude": prop.get("location", {}).get("latitude"),
        "longitude": prop.get("location", {}).get("longitude"),
        "description": prop.get("propertyTypeFullDescription"),
        "property_url": prop.get("propertyUrl")
    }

output = []
start = 3
end = 6  # exclusive
for borough_name, postcode_list in boroughs.items():
    ## randomize to avoid bias
    if borough_name!= "Camden" and borough_name!= "City of London" and borough_name!="Ealing" and borough_name!='Haringey':
        random_postcodes = random.sample(postcode_list, k=min(len(postcode_list), 20)) 
        for postcode in random_postcodes:  # can be limited to first 3 postcodes to avoid hammering
            clean_postcode = postcode.replace(" ", "").upper()  # remove spaces & uppercase
            location_identifier = f"POSTCODE^{clean_postcode}"
            encoded_location_identifier = quote_plus(location_identifier)  # URL encode
            # Sample random unique pages to scrape
            pages_to_scrape = random.sample(range(max_pages_per_postcode), pages_per_postcode_to_sample)
            pages_to_scrape.sort()  
            for page_num in pages_to_scrape:
                index = page_num * page_size
                url = f"https://www.rightmove.co.uk/api/property-search/listing/search?searchLocation=London&useLocationIdentifier=true&locationIdentifier=REGION%5E87490&radius=0.0&_includeLetAgreed=on&index={index}&sortType=6&channel=RENT&transactionType=LETTING"
                print(f"Scraping: {borough_name} - Postcode: {postcode} - Page: {page_num}")
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        properties = data.get("properties", [])
                        if not properties:
                            print(f"No properties found for {postcode} page {page_num}")
                            continue
                        trimmed = [extract_minimal_fields(p) for p in properties]
                        df_properties = pd.json_normalize(trimmed)
                        df_properties["borough"] = borough_name
                        df_properties["postcode"] = postcode
                        df_properties["page"] = page_num
                        output.append(df_properties)
                    ##time.sleep(SLEEP_TIME)
                    except Exception as e:
                        print(f"Failed to parse json for {postcode} page {page_num}: {e}")
                else:
                    print(f"Failed to fetch {postcode} page {page_num}: HTTP {response.status_code}")
            
            #time.sleep(SLEEP_TIME)



master_path="./combined_listings_deduped2.csv"
master_df= pd.read_csv(master_path)
existing_ids = set(master_df['id'].astype(str))
if output:
    final_df = pd.concat(output)
    ## convert id to string to match exisiting ids type
    final_df['id'] = final_df['id'].astype(str)
      ##filter out already scraped listing by id
    final_df=final_df[~final_df['id'].isin(existing_ids)]

   
    final_df['date_listed']= pd.to_datetime(final_df['date_listed'], errors='coerce').dt.date
    cutoff_date = (datetime.now(timezone.utc) - timedelta(days=180)).date()
    final_df = final_df[final_df["date_listed"] >= cutoff_date]
    if not final_df.empty:
          # filter only listings before jan 1, 2025
        updated_master_df= pd.concat([master_df,final_df])
        updated_master_df.drop_duplicates(subset='id',inplace=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   
        updated_master_df.to_csv(master_path, index=False)        
    else:
          print("No new unique listings to save after filtering duplicates.")
    
else:
    print("NO data was scraped")


