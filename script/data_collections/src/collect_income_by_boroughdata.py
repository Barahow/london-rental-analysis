import pandas as pd
import glob

# load boroughs and their postcodes
boroughs_df = pd.read_csv("./borough_postcodes.csv")  # Replace with your actual filename

# Create list of inner london borugh names
inner_london_boroughs = boroughs_df["borough"].tolist()


## load all csvs into a single datafram

xls = pd.ExcelFile("./income_per_borough.xlsx")

#print(xls.sheet_names)
income_df = pd.read_excel(xls,sheet_name="Total, weekly",header=[0,1])


## flatten the multiindex columns: e.g. (2024,pay)-> 2024_pay
income_df.columns= [
f"{a}_{b}".strip("_") for a,b in income_df.columns


]

print(income_df.columns.tolist())

##keep only inner london broughs 

inner_df = income_df[income_df["Area_Unnamed: 1_level_1"].isin(inner_london_boroughs)].copy()



##Extract just the borough name, the year, and the 2024 median pay
result_df = inner_df[["Area_Unnamed: 1_level_1","2024_Pay (£)"]].rename(
    columns={"Area_Unnamed: 1_level_1":"borough","2024_Pay (£)":"median_income"}
)
result_df["year"]=2024

result_df= result_df[["borough","year","median_income"]]


## remove the bad city of london row 
result_df = result_df[result_df["borough"]!="City of London"]
## the excel sheet didnt have the numbers for city of london
## so, i found the median income for city of london online
## manually insert it into the data
city_row = pd.DataFrame([

    {"borough":"City of London",
     "year":2024,
     "median_income":853.4
     
     
     }
])

result_df= pd.concat([result_df,city_row],ignore_index=True)

print(result_df)


result_df.to_csv("income_by_borough.csv",index=False)
