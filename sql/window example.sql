

--Rank borough per rent per mounth
select borough, price_amount,
dense_rank() over(partition by borough order by price_amount desc) as price_rank
from fact_listings
