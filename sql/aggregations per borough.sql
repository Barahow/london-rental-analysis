

-- Get the top 5 rents by borough
select top 5 borough, avg(price_amount) as avg_price
from fact_listings
group by borough
order by avg_price desc

--Count listing by borough 
select borough, count(*) as listings_count
from fact_listings
group by borough
order by listings_count desc