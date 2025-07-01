


select * from fact_listings fl
left join gcse_dim gd
on fl.borough= gd.borough


select * from fact_listings fl
left join employment_rate_dim erd
on fl.borough= erd.borough

select * from fact_listings fl 
left join crime_rate_dim crd
on fl.borough=crd.borough