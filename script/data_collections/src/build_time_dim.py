import pandas as pd 
from datetime import datetime,timedelta,timezone

## calculate date range 
end_date = datetime.now(timezone.utc).date()
start_date = end_date - timedelta(days=180)

## create data range 
dates = pd.date_range(start=start_date,end=end_date)

##build dataframe
time_dim = pd.DataFrame({
    "date":dates,
    "year": dates.year,
    "month":dates.month,
    "quarter":dates.quarter,
    "day_of_week": dates.day_name()


})


## save tp csv
time_dim.to_csv("time_dim.csv",index=False)