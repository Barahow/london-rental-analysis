import pandas as pd
import os 
import numpy as np 

print("=== London Rental Market Analysis - Data Collection ===")
print("Chunk 1: Setup Complete")
print(f"Pandas version: {pd.__version__}")
print(f"Working directory: {os.getcwd()}")

if not os.path.exists('../data'):
    os.makedirs('../data')
    print("Created data folder")
else:
    print("Data folder exists")


##extract the required onspd columns 

required_colums= {
    'pcd':0, ## Unit postcode – 7 character version (1st column)
    'oslaua':7, ### Local Authority District (8th column) 
    'osward':8 ### Electoral Ward/Division (9th column)

}

# Inner London borough codes (ONS Local Authority codes)
inner_london_codes = {
  'E09000001': 'City of London',
    'E09000007': 'Camden', 
    'E09000009': 'Ealing',
    'E09000012': 'Hackney',
    'E09000013': 'Hammersmith and Fulham',
    'E09000014': 'Haringey',
    'E09000019': 'Islington',
    'E09000020': 'Kensington and Chelsea',
    'E09000022': 'Lambeth',
    'E09000023': 'Lewisham',
    'E09000025': 'Newham',
    'E09000028': 'Southwark',
    'E09000030': 'Tower Hamlets',
    'E09000032': 'Wandsworth',
    'E09000033': 'Westminster'

}

print("Required colums in the project")

for col_name, position in required_colums.items():
    description = {
        'pcd':'Postcode',
        'oslaua': 'Local Authority (Borough)',
        'osward': 'Electoral Ward'
    }
    print(f" - {col_name} (position {position}): {description[col_name]}")


# When reading and filtering the CSV:
columns_to_extract = ['pcd', 'oslaua', 'osward']



## read only necessary columns using column index mapping 
usecols = list(required_colums.values())
col_names = list(required_colums.keys())

## read and rename columns properly 
def load_post_code_data(filepath):
    df = pd.read_csv(filepath, header=None,usecols=usecols)
    df.columns= col_names
    return df

def load_ward_data(filepath):
    ward_df=pd.read_csv(filepath)
    return ward_df[['WD23CD','WD23NM','WD23NMW']]


def filter_inner_london(df,borough_codes):
    return df[df['oslaua'].isin(borough_codes.keys())].copy()


def map_wards(filtered_df,ward_df,borough_codes):
    ward_mapping= ward_df.set_index('WD23CD')['WD23NM'].to_dict()
    filtered_df['borough']= filtered_df['oslaua'].map(borough_codes)
    filtered_df['ward']= filtered_df['osward'].map(ward_mapping)
    return filtered_df

def resolve_path(relative_path):
    # Always resolve path relative to the current .py file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)
import json
def main():
 
   post_code_path = resolve_path("../data/postcode_lookup_inner_london.csv")
   ward_path = resolve_path("../data/ward_names.csv")
   postcode_df=load_post_code_data(post_code_path)
   ward_df = load_ward_data(ward_path)
   filtered_df = filter_inner_london(postcode_df,inner_london_codes)
   
 
   mapped_df =map_wards(filtered_df,ward_df,inner_london_codes)
   mapped_df = mapped_df.drop_duplicates(subset=['pcd', 'borough', 'ward'])
   print(mapped_df[['pcd','borough','ward']].head())
   # Remove duplicates just in case
   mapped_df = mapped_df.drop_duplicates(subset=['pcd', 'borough', 'ward'])

# Group postcodes by borough as lists of strings (like "SW16 5TB")
   postcodes_by_borough = mapped_df.groupby('borough')['pcd'].apply(lambda x: sorted(x.unique())).to_dict()
    


# Print example output
   for borough, postcodes in postcodes_by_borough.items():
       print(f'"{borough}": {postcodes[:5]}')  # print first 5 postcodes for brevity



# Ensure all postcodes are sorted strings
   for b, pcodes in postcodes_by_borough.items():
    postcodes_by_borough[b] = sorted([str(p).strip() for p in pcodes])

# Dump as a pretty-printed dictionary string
   formatted = json.dumps(postcodes_by_borough, indent=4)

   print(f"boroughs = {formatted}")
   output_path = resolve_path("../data/postcodes_lookup.csv")
   mapped_df[['pcd', 'ward', 'borough']].to_csv(output_path, index=False)
   print(f"\n✅ CSV saved to {output_path}")

   with open("borough_postcodes.py", "w") as f:
    f.write("boroughs = ")
    f.write(json.dumps(postcodes_by_borough, indent=4))




if __name__== "__main__":
    main()

