

-- Categorize affordability based on ratios
select id, price_amount, monthly_income,
case when price_amount/monthly_income <0.3 then 'Affordable'
     when price_amount/monthly_income between 0.3 and 0.5 then 'Borderline'
     else 'Unaffordable' 
end as affordability_category 
from fact_listings