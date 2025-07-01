

-- Index for faster lookup by borough 
Create nonclustered index idx_borough on fact_listings(borough)