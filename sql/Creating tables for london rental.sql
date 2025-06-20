

create Database LondonRentalDB;
use londonrentalDB
-- table 1
CREATE TABLE listings_raw (
    listing_id INT PRIMARY KEY,
    postcode VARCHAR(10),
    borough VARCHAR(50),
    bedrooms INT,
    rent_price DECIMAL(10, 2),
    size_sqft DECIMAL(10, 2),
    date_listed DATE
);
-- Table 2: postcodes_lookup
CREATE TABLE postcodes_lookup (
    postcode VARCHAR(10) PRIMARY KEY,
    ward VARCHAR(100),
    borough VARCHAR(50)
);

-- Table 4: boroughs
CREATE TABLE boroughs (
    borough VARCHAR(50) PRIMARY KEY,
    region VARCHAR(20),  
    zone INT,
    population INT
);

CREATE TABLE income_by_borough (
    borough VARCHAR(50),
    year INT,
    median_income DECIMAL(10, 2),
    PRIMARY KEY (borough, year)
);


-- Table 6: time_dim
CREATE TABLE time_dim (
    date DATE PRIMARY KEY,
    year INT,
    month INT,
    quarter INT,
    day_of_week VARCHAR(10)
);


