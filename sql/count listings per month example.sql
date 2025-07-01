

-- Listings count per month 
select format(date_listed,'yyyy-MM') as month, count(*) listings 
from fact_listings
group by format(date_listed,'yyyy-MM')
order by month