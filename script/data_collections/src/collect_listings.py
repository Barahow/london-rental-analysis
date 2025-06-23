

import pandas as pd
import glob


## load all csvs into a single datafram

files = glob.glob("./listings_raw*.csv")
df_list = [pd.read_csv(file) for file in files]
combined_df = pd.concat(df_list,ignore_index=True)



## check for duplicates 

## count toal vs unqiue 
total_records=len(combined_df)
unique_records= combined_df['id'].nunique()
duplicate_count= total_records-unique_records
## drop duplicates 
combined_df.drop_duplicates(subset='id',inplace=True)

total_records_after = len(combined_df)
print(f"Total records: {total_records}")
print(f"Unique listings: {unique_records}")
print(f"Duplicate listings: {duplicate_count}")
# Recalculate total after dropping

print(f"No duplicates {total_records_after} ")


# Group by borough and count unique listings
borough_counts = combined_df.groupby('borough')['id'].nunique().sort_values(ascending=True)

# Display boroughs with the fewest listings
print("Listings per borough (ascending):")
print(borough_counts)
# Assuming combined_df is already deduplicated (no duplicate 'id's)
combined_df.to_csv("lisings_new.csv", index=False)
