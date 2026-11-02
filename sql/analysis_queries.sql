-- =============================================================================
-- SQL BUSINESS QUERIES: analysis_queries.sql
-- PROJECT: Automotive Dealership Profitability & Working Capital Analysis
-- DATABASE: SQLite 3 (dealership.db)
-- DATASET: Real CarDekho Vehicle Listings (6,926 Cleaned Unique Vehicles)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Query 1: Average Selling Price by Brand (Ranked by Total Listing Volume)
-- -----------------------------------------------------------------------------
SELECT 
    Vehicle_Brand,
    COUNT(*) AS total_listings,
    ROUND(AVG(selling_price), 2) AS avg_selling_price_inr,
    ROUND(MIN(selling_price), 2) AS min_selling_price_inr,
    ROUND(MAX(selling_price), 2) AS max_selling_price_inr,
    ROUND(SUM(selling_price) / 10000000.0, 2) AS total_market_value_cr
FROM vehicles
GROUP BY Vehicle_Brand
ORDER BY total_listings DESC;

-- -----------------------------------------------------------------------------
-- Query 2: Top 10 Highest-Priced Vehicles in the Marketplace
-- -----------------------------------------------------------------------------
SELECT 
    name,
    Vehicle_Brand,
    Vehicle_Model,
    year,
    selling_price,
    km_driven,
    fuel,
    transmission
FROM vehicles
ORDER BY selling_price DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- Query 3: Top 10 Lowest-Priced (Budget / Liquidation) Vehicles
-- -----------------------------------------------------------------------------
SELECT 
    name,
    Vehicle_Brand,
    Vehicle_Model,
    year,
    selling_price,
    km_driven,
    fuel,
    owner
FROM vehicles
ORDER BY selling_price ASC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- Query 4: Average Price and Fuel Economy by Fuel Type
-- -----------------------------------------------------------------------------
SELECT 
    Fuel_Category,
    COUNT(*) AS total_listings,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vehicles), 2) AS share_pct,
    ROUND(AVG(selling_price), 2) AS avg_selling_price_inr,
    ROUND(AVG(Mileage_kmpl), 2) AS avg_fuel_efficiency_kmpl,
    ROUND(AVG(km_driven), 0) AS avg_odometer_km
FROM vehicles
GROUP BY Fuel_Category
ORDER BY total_listings DESC;

-- -----------------------------------------------------------------------------
-- Query 5: Average Price and Valuation Premium by Transmission
-- -----------------------------------------------------------------------------
SELECT 
    Transmission_Category,
    COUNT(*) AS total_listings,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vehicles), 2) AS share_pct,
    ROUND(AVG(selling_price), 2) AS avg_selling_price_inr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven,
    ROUND(AVG(Vehicle_Age), 1) AS avg_vehicle_age_yrs
FROM vehicles
GROUP BY Transmission_Category;

-- -----------------------------------------------------------------------------
-- Query 6: Average Price and Depreciation Discount by Ownership Category
-- -----------------------------------------------------------------------------
SELECT 
    Ownership_Category,
    COUNT(*) AS total_listings,
    ROUND(AVG(selling_price), 2) AS avg_selling_price_inr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven,
    ROUND(AVG(Vehicle_Age), 1) AS avg_vehicle_age_yrs
FROM vehicles
GROUP BY Ownership_Category
ORDER BY avg_selling_price_inr DESC;

-- -----------------------------------------------------------------------------
-- Query 7: Dealer vs Individual Listing Comparison (Channel Analysis)
-- -----------------------------------------------------------------------------
SELECT 
    Seller_Category,
    COUNT(*) AS total_listings,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vehicles), 2) AS share_pct,
    ROUND(AVG(selling_price), 2) AS avg_asking_price_inr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven,
    ROUND(AVG(Vehicle_Age), 1) AS avg_vehicle_age_yrs
FROM vehicles
GROUP BY Seller_Category
ORDER BY avg_asking_price_inr DESC;

-- -----------------------------------------------------------------------------
-- Query 8: Brand-Wise Vehicle Distribution & Cumulative Market Concentration
-- -----------------------------------------------------------------------------
WITH BrandVolume AS (
    SELECT 
        Vehicle_Brand,
        COUNT(*) AS brand_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vehicles), 2) AS volume_share_pct
    FROM vehicles
    GROUP BY Vehicle_Brand
)
SELECT 
    Vehicle_Brand,
    brand_count,
    volume_share_pct,
    ROUND(SUM(volume_share_pct) OVER (ORDER BY brand_count DESC), 2) AS cumulative_share_pct
FROM BrandVolume
ORDER BY brand_count DESC
LIMIT 15;

-- -----------------------------------------------------------------------------
-- Query 9: Vehicle Age Cohort Analysis (Valuation & Odometer by Age Bracket)
-- -----------------------------------------------------------------------------
SELECT 
    Vehicle_Age_Group,
    COUNT(*) AS listing_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vehicles), 2) AS cohort_pct,
    ROUND(AVG(selling_price), 2) AS avg_price_inr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven,
    MIN(Vehicle_Age) AS min_cohort_age,
    MAX(Vehicle_Age) AS max_cohort_age
FROM vehicles
GROUP BY Vehicle_Age_Group
ORDER BY min_cohort_age ASC;

-- -----------------------------------------------------------------------------
-- Query 10: Price Distribution by Manufacturing Year (Depreciation Curve)
-- -----------------------------------------------------------------------------
SELECT 
    year,
    2026 - year AS vehicle_age_yrs,
    COUNT(*) AS listings_count,
    ROUND(AVG(selling_price), 2) AS avg_price_inr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven
FROM vehicles
WHERE year >= 2005
GROUP BY year
ORDER BY year DESC;

-- -----------------------------------------------------------------------------
-- Query 11: Top 10 Vehicles with Highest Kilometres Driven (Fleet / Road Warriors)
-- -----------------------------------------------------------------------------
SELECT 
    name,
    Vehicle_Brand,
    year,
    km_driven,
    selling_price,
    fuel,
    owner
FROM vehicles
ORDER BY km_driven DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- Query 12: Price Category Distribution (Dealership Tier Segmentation)
-- -----------------------------------------------------------------------------
SELECT 
    Price_Category,
    COUNT(*) AS inventory_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vehicles), 2) AS volume_pct,
    ROUND(SUM(selling_price) / 10000000.0, 2) AS total_inventory_value_cr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven,
    ROUND(AVG(Vehicle_Age), 1) AS avg_age_yrs
FROM vehicles
GROUP BY Price_Category
ORDER BY total_inventory_value_cr DESC;

-- -----------------------------------------------------------------------------
-- Query 13: Fuel Type Distribution Cross-Tabulated with Transmission
-- -----------------------------------------------------------------------------
SELECT 
    Fuel_Category,
    Transmission_Category,
    COUNT(*) AS listing_count,
    ROUND(AVG(selling_price), 2) AS avg_price_inr
FROM vehicles
GROUP BY Fuel_Category, Transmission_Category
ORDER BY Fuel_Category, listing_count DESC;

-- -----------------------------------------------------------------------------
-- Query 14: Transmission Distribution Across Odometer Usage Tiers
-- -----------------------------------------------------------------------------
SELECT 
    Kilometres_Category,
    Transmission_Category,
    COUNT(*) AS listing_count,
    ROUND(AVG(selling_price), 2) AS avg_price_inr
FROM vehicles
GROUP BY Kilometres_Category, Transmission_Category
ORDER BY Kilometres_Category, listing_count DESC;

-- -----------------------------------------------------------------------------
-- Query 15: Brand-Wise Median Selling Price (Rank-Based Quartile Approximation)
-- -----------------------------------------------------------------------------
WITH RankedBrandPrices AS (
    SELECT 
        Vehicle_Brand,
        selling_price,
        ROW_NUMBER() OVER (PARTITION BY Vehicle_Brand ORDER BY selling_price) AS row_num,
        COUNT(*) OVER (PARTITION BY Vehicle_Brand) AS total_rows
    FROM vehicles
)
SELECT 
    Vehicle_Brand,
    total_rows AS brand_volume,
    ROUND(AVG(selling_price), 2) AS approximate_median_price_inr
FROM RankedBrandPrices
WHERE row_num IN ((total_rows + 1) / 2, (total_rows + 2) / 2)
GROUP BY Vehicle_Brand, total_rows
HAVING total_rows >= 50
ORDER BY approximate_median_price_inr DESC;

-- -----------------------------------------------------------------------------
-- Query 16: Top 10 Most Expensive Vehicle Models (Minimum 10 Listings Liquidity)
-- -----------------------------------------------------------------------------
SELECT 
    Vehicle_Brand,
    Vehicle_Model,
    COUNT(*) AS sample_size,
    ROUND(AVG(selling_price), 2) AS avg_selling_price_inr,
    ROUND(MIN(selling_price), 2) AS min_model_price_inr,
    ROUND(MAX(selling_price), 2) AS max_model_price_inr
FROM vehicles
GROUP BY Vehicle_Brand, Vehicle_Model
HAVING COUNT(*) >= 10
ORDER BY avg_selling_price_inr DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- Query 17: Vehicle Age and Price Correlation Analysis (Price Retention by Age)
-- -----------------------------------------------------------------------------
SELECT 
    Vehicle_Age,
    COUNT(*) AS listing_count,
    ROUND(AVG(selling_price), 2) AS avg_price_inr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven,
    ROUND(
        (AVG(selling_price) - LAG(AVG(selling_price)) OVER (ORDER BY Vehicle_Age ASC)) 
        / LAG(AVG(selling_price)) OVER (ORDER BY Vehicle_Age ASC) * 100.0, 
        2
    ) AS yoy_depreciation_pct
FROM vehicles
WHERE Vehicle_Age BETWEEN 6 AND 18
GROUP BY Vehicle_Age
ORDER BY Vehicle_Age ASC;

-- -----------------------------------------------------------------------------
-- Query 18: Ownership and Price Interaction Analysis across Top 5 Brands
-- -----------------------------------------------------------------------------
SELECT 
    Vehicle_Brand,
    Ownership_Category,
    COUNT(*) AS listing_count,
    ROUND(AVG(selling_price), 2) AS avg_price_inr
FROM vehicles
WHERE Vehicle_Brand IN ('Maruti', 'Hyundai', 'Mahindra', 'Tata', 'Toyota')
GROUP BY Vehicle_Brand, Ownership_Category
ORDER BY Vehicle_Brand, avg_price_inr DESC;

-- -----------------------------------------------------------------------------
-- Query 19: Seller Category and Vehicle Price Dispersion Analysis
-- -----------------------------------------------------------------------------
SELECT 
    Seller_Category,
    COUNT(*) AS volume,
    ROUND(MIN(selling_price), 2) AS min_price_inr,
    ROUND(AVG(selling_price), 2) AS avg_price_inr,
    ROUND(MAX(selling_price), 2) AS max_price_inr,
    ROUND(
        SQRT(AVG(selling_price * selling_price) - AVG(selling_price) * AVG(selling_price)), 
        2
    ) AS std_dev_price_inr
FROM vehicles
GROUP BY Seller_Category;

-- -----------------------------------------------------------------------------
-- Query 20: Comprehensive Market Segment Matrix (Fuel, Transmission, Seller)
-- -----------------------------------------------------------------------------
SELECT 
    Fuel_Category,
    Transmission_Category,
    Seller_Category,
    COUNT(*) AS total_units,
    ROUND(AVG(selling_price), 2) AS avg_price_inr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven
FROM vehicles
GROUP BY Fuel_Category, Transmission_Category, Seller_Category
HAVING COUNT(*) >= 25
ORDER BY total_units DESC;
