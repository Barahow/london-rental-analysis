
CREATE VIEW vw_borough_summary as 
select borough,
count(*) as total_listings,
avg(price_amount) as avg_rent,
avg(monthly_income) as avg_income
from fact_listings
group by borough 


select * from  vw_borough_summary