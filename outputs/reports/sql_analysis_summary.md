# AUTOMOTIVE DEALERSHIP SQL BUSINESS ANALYSIS REPORT

**Source Database:** `dealership.db` | **Cleaned Population:** 6,926 Real Vehicles

## Query 1: Average Selling Price by Brand (Ranked by Total Listing Volume)

```sql
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
```

**Results (32 rows):**

| Vehicle_Brand | total_listings | avg_selling_price_inr | min_selling_price_inr | max_selling_price_inr | total_market_value_cr |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Maruti | 2165 | 387821.62 | 29999.0 | 1200000.0 | 83.96 |
| Hyundai | 1267 | 451051.64 | 30000.0 | 1950000.0 | 57.15 |
| Mahindra | 723 | 616549.06 | 120000.0 | 1800000.0 | 44.58 |
| Tata | 647 | 344393.98 | 40000.0 | 1700000.0 | 22.28 |
| Honda | 362 | 573563.91 | 50000.0 | 2125000.0 | 20.76 |
| Ford | 361 | 504376.69 | 55000.0 | 3250000.0 | 18.21 |
| Toyota | 357 | 889490.13 | 100000.0 | 3500000.0 | 31.75 |
| Chevrolet | 216 | 268349.63 | 45000.0 | 1295000.0 | 5.8 |
| Renault | 206 | 449694.14 | 200000.0 | 1265000.0 | 9.26 |
| Volkswagen | 174 | 489574.7 | 210000.0 | 2150000.0 | 8.52 |
| Nissan | 73 | 456616.38 | 110000.0 | 1200000.0 | 3.33 |
| Skoda | 70 | 591442.81 | 100000.0 | 3251000.0 | 4.14 |
| Datsun | 57 | 316017.49 | 150000.0 | 590000.0 | 1.8 |
| Bmw | 47 | 2770638.3 | 480000.0 | 7200000.0 | 13.02 |
| Mercedes-Benz | 46 | 2253347.83 | 400000.0 | 6000000.0 | 10.37 |
| Fiat | 44 | 295340.86 | 70000.0 | 700000.0 | 1.3 |
| Audi | 33 | 2422363.55 | 730000.0 | 6523000.0 | 7.99 |
| Jeep | 22 | 1789227.23 | 1325000.0 | 4100000.0 | 3.94 |
| Mitsubishi | 11 | 758636.36 | 150000.0 | 1950000.0 | 0.83 |
| Volvo | 9 | 4036111.11 | 1200000.0 | 10000000.0 | 3.63 |
| Jaguar | 8 | 2748250.0 | 2000000.0 | 3500000.0 | 2.2 |
| Ambassador | 4 | 124000.0 | 75000.0 | 200000.0 | 0.05 |
| Force | 4 | 841250.0 | 555000.0 | 1050000.0 | 0.34 |
| Isuzu | 4 | 1752500.0 | 1160000.0 | 2700000.0 | 0.7 |
| Daewoo | 3 | 77000.0 | 45000.0 | 100000.0 | 0.02 |
| Kia | 3 | 1372666.67 | 643000.0 | 1900000.0 | 0.41 |
| Land Rover | 3 | 2716666.67 | 1650000.0 | 4500000.0 | 0.81 |
| Mg | 3 | 1783333.33 | 1700000.0 | 1900000.0 | 0.54 |
| Ashok Leyland | 1 | 300000.0 | 300000.0 | 300000.0 | 0.03 |
| Lexus | 1 | 5150000.0 | 5150000.0 | 5150000.0 | 0.52 |
| Opel | 1 | 68000.0 | 68000.0 | 68000.0 | 0.01 |
| Peugeot | 1 | 57000.0 | 57000.0 | 57000.0 | 0.01 |

## Query 2: Top 10 Highest-Priced Vehicles in the Marketplace

```sql
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
```

**Results (10 rows):**

| name | Vehicle_Brand | Vehicle_Model | year | selling_price | km_driven | fuel | transmission |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Volvo XC90 T8 Excellence BSIV | Volvo | XC90 T8 | 2017 | 10000000.0 | 30000.0 | Petrol | Automatic |
| BMW X7 xDrive 30d DPE | Bmw | X7 xDrive | 2020 | 7200000.0 | 5000.0 | Diesel | Automatic |
| Audi A6 35 TFSI Matrix | Audi | A6 35 | 2019 | 6523000.0 | 23600.0 | Petrol | Automatic |
| Audi A6 35 TFSI Matrix | Audi | A6 35 | 2019 | 6223000.0 | 7800.0 | Petrol | Automatic |
| BMW 6 Series GT 630d Luxury Line | Bmw | 6 Series | 2018 | 6000000.0 | 27000.0 | Diesel | Automatic |
| BMW 6 Series GT 630d Luxury Line | Bmw | 6 Series | 2018 | 6000000.0 | 28156.0 | Diesel | Automatic |
| Mercedes-Benz S-Class S 350 CDI | Mercedes-Benz | S-Class S | 2017 | 6000000.0 | 37000.0 | Diesel | Automatic |
| Audi A6 35 TFSI Matrix | Audi | A6 35 | 2019 | 5923000.0 | 11500.0 | Petrol | Automatic |
| Mercedes-Benz S-Class S 350 CDI | Mercedes-Benz | S-Class S | 2017 | 5850000.0 | 47000.0 | Diesel | Automatic |
| BMW 6 Series GT 630d Luxury Line | Bmw | 6 Series | 2018 | 5830000.0 | 30000.0 | Diesel | Automatic |

## Query 3: Top 10 Lowest-Priced (Budget / Liquidation) Vehicles

```sql
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
```

**Results (10 rows):**

| name | Vehicle_Brand | Vehicle_Model | year | selling_price | km_driven | fuel | owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Maruti 800 AC | Maruti | 800 AC | 1997 | 29999.0 | 80000.0 | Petrol | Third Owner |
| Maruti Zen LXI | Maruti | Zen | 2001 | 30000.0 | 10000.0 | Petrol | First Owner |
| Hyundai Santro GLS I - Euro I | Hyundai | Santro GLS | 2000 | 30000.0 | 90000.0 | Petrol | Third Owner |
| Maruti 800 Std | Maruti | 800 Std | 2000 | 31000.0 | 56194.0 | Petrol | Fourth & Above Owner |
| Maruti 800 Std | Maruti | 800 Std | 2004 | 31504.0 | 110000.0 | Petrol | Third Owner |
| Maruti Wagon R VXI | Maruti | Wagon R | 2004 | 33351.0 | 90000.0 | Petrol | Third Owner |
| Hyundai Santro LE | Hyundai | Santro LE | 2001 | 33983.0 | 80000.0 | Petrol | Second Owner |
| Maruti 800 Std BSII | Maruti | 800 Std | 2003 | 35000.0 | 35000.0 | Petrol | Second Owner |
| Maruti 800 AC | Maruti | 800 AC | 2007 | 35000.0 | 10000.0 | Petrol | First Owner |
| Hyundai Santro LE | Hyundai | Santro LE | 2002 | 35000.0 | 184000.0 | Petrol | Second Owner |

## Query 4: Average Price and Fuel Economy by Fuel Type

```sql
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
```

**Results (4 rows):**

| Fuel_Category | total_listings | share_pct | avg_selling_price_inr | avg_fuel_efficiency_kmpl | avg_odometer_km |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Diesel | 3755 | 54.22 | 639727.77 | 19.74 | 88702.0 |
| Petrol | 3077 | 44.43 | 375688.97 | 19.06 | 55947.0 |
| Cng | 56 | 0.81 | 300499.95 | 23.99 | 69329.0 |
| Lpg | 38 | 0.55 | 200421.05 | 18.58 | 89174.0 |

## Query 5: Average Price and Valuation Premium by Transmission

```sql
SELECT 
    Transmission_Category,
    COUNT(*) AS total_listings,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vehicles), 2) AS share_pct,
    ROUND(AVG(selling_price), 2) AS avg_selling_price_inr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven,
    ROUND(AVG(Vehicle_Age), 1) AS avg_vehicle_age_yrs
FROM vehicles
GROUP BY Transmission_Category;
```

**Results (2 rows):**

| Transmission_Category | total_listings | share_pct | avg_selling_price_inr | avg_km_driven | avg_vehicle_age_yrs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Automatic | 584 | 8.43 | 1309712.3 | 51178.0 | 10.7 |
| Manual | 6342 | 91.57 | 444299.07 | 76097.0 | 12.8 |

## Query 6: Average Price and Depreciation Discount by Ownership Category

```sql
SELECT 
    Ownership_Category,
    COUNT(*) AS total_listings,
    ROUND(AVG(selling_price), 2) AS avg_selling_price_inr,
    ROUND(AVG(km_driven), 0) AS avg_km_driven,
    ROUND(AVG(Vehicle_Age), 1) AS avg_vehicle_age_yrs
FROM vehicles
GROUP BY Ownership_Category
ORDER BY avg_selling_price_inr DESC;
```

**Results (5 rows):**

| Ownership_Category | total_listings | avg_selling_price_inr | avg_km_driven | avg_vehicle_age_yrs |
| :--- | :--- | :--- | :--- | :--- |
| Test Drive Car | 5 | 4403800.0 | 14631.0 | 7.0 |
| First Owner | 4242 | 615404.4 | 61634.0 | 11.1 |
| Second Owner | 1974 | 385697.19 | 90765.0 | 14.4 |
| Third Owner | 536 | 281250.95 | 100180.0 | 16.4 |
| Fourth & Above Owner | 169 | 224470.37 | 107120.0 | 18.0 |

## Query 7: Dealer vs Individual Listing Comparison (Channel Analysis)

```sql
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
```

**Results (3 rows):**

| Seller_Category | total_listings | share_pct | avg_asking_price_inr | avg_km_driven | avg_vehicle_age_yrs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Dealer | 681 | 9.83 | 926722.42 | 52666.0 | 10.8 |
| Trustmark Dealer | 27 | 0.39 | 718111.11 | 36335.0 | 9.6 |
| Individual | 6218 | 89.78 | 471555.12 | 76495.0 | 12.8 |

## Query 8: Brand-Wise Vehicle Distribution & Cumulative Market Concentration

```sql
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
```

**Results (15 rows):**

| Vehicle_Brand | brand_count | volume_share_pct | cumulative_share_pct |
| :--- | :--- | :--- | :--- |
| Maruti | 2165 | 31.26 | 31.26 |
| Hyundai | 1267 | 18.29 | 49.55 |
| Mahindra | 723 | 10.44 | 59.99 |
| Tata | 647 | 9.34 | 69.33 |
| Honda | 362 | 5.23 | 74.56 |
| Ford | 361 | 5.21 | 79.77 |
| Toyota | 357 | 5.15 | 84.92 |
| Chevrolet | 216 | 3.12 | 88.04 |
| Renault | 206 | 2.97 | 91.01 |
| Volkswagen | 174 | 2.51 | 93.52 |
| Nissan | 73 | 1.05 | 94.57 |
| Skoda | 70 | 1.01 | 95.58 |
| Datsun | 57 | 0.82 | 96.4 |
| Bmw | 47 | 0.68 | 97.08 |
| Mercedes-Benz | 46 | 0.66 | 97.74 |

## Query 9: Vehicle Age Cohort Analysis (Valuation & Odometer by Age Bracket)

```sql
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
```

**Results (4 rows):**

| Vehicle_Age_Group | listing_count | cohort_pct | avg_price_inr | avg_km_driven | min_cohort_age | max_cohort_age |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Under 7 Years (Recent) | 410 | 5.92 | 940246.3 | 19316.0 | 6 | 7 |
| 7 to 10 Years (Mid-Age) | 2109 | 30.45 | 745000.44 | 48805.0 | 8 | 10 |
| 11 to 15 Years (Mature) | 2982 | 43.06 | 449684.72 | 86115.0 | 11 | 15 |
| Over 15 Years (Aged) | 1425 | 20.57 | 199964.89 | 101650.0 | 16 | 43 |

## Query 10: Price Distribution by Manufacturing Year (Depreciation Curve)

```sql
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
```

**Results (16 rows):**

| year | vehicle_age_yrs | listings_count | avg_price_inr | avg_km_driven |
| :--- | :--- | :--- | :--- | :--- |
| 2020.0 | 6.0 | 63.0 | 888349.16 | 20641.0 |
| 2019.0 | 7.0 | 347.0 | 949668.55 | 19076.0 |
| 2018.0 | 8.0 | 608.0 | 866376.61 | 34938.0 |
| 2017.0 | 9.0 | 808.0 | 732419.52 | 48582.0 |
| 2016.0 | 10.0 | 693.0 | 653180.34 | 61230.0 |
| 2015.0 | 11.0 | 681.0 | 589177.63 | 70939.0 |
| 2014.0 | 12.0 | 581.0 | 511858.8 | 79416.0 |
| 2013.0 | 13.0 | 562.0 | 451501.72 | 88866.0 |
| 2012.0 | 14.0 | 604.0 | 351387.38 | 96478.0 |
| 2011.0 | 15.0 | 554.0 | 318335.7 | 97706.0 |
| 2010.0 | 16.0 | 380.0 | 273897.33 | 101862.0 |
| 2009.0 | 17.0 | 240.0 | 227691.62 | 99471.0 |
| 2008.0 | 18.0 | 205.0 | 208397.64 | 98479.0 |
| 2007.0 | 19.0 | 176.0 | 174894.51 | 114964.0 |
| 2006.0 | 20.0 | 123.0 | 164383.31 | 105180.0 |
| 2005.0 | 21.0 | 91.0 | 137994.49 | 100076.0 |

## Query 11: Top 10 Vehicles with Highest Kilometres Driven (Fleet / Road Warriors)

```sql
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
```

**Results (10 rows):**

| name | Vehicle_Brand | year | km_driven | selling_price | fuel | owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Hyundai i20 Asta 1.2 | Hyundai | 2007 | 2360457.0 | 550000.0 | Petrol | Second Owner |
| Mahindra XUV500 W6 2WD | Mahindra | 2012 | 1500000.0 | 500000.0 | Diesel | First Owner |
| Maruti Wagon R LXI Minor | Maruti | 2010 | 577414.0 | 194000.0 | Petrol | Second Owner |
| Maruti Wagon R VXI BS IV | Maruti | 2011 | 500000.0 | 229999.0 | Petrol | Second Owner |
| Toyota Innova 2.5 EV Diesel PS 7 Seater BSIII | Toyota | 2011 | 500000.0 | 350000.0 | Diesel | Second Owner |
| Mahindra Scorpio M2DI | Mahindra | 2011 | 475000.0 | 400000.0 | Diesel | Third Owner |
| Toyota Innova 2.5 VX (Diesel) 7 Seater | Toyota | 2013 | 440000.0 | 750000.0 | Diesel | Second Owner |
| Toyota Innova 2.5 VX (Diesel) 7 Seater BS IV | Toyota | 2010 | 426000.0 | 950000.0 | Diesel | First Owner |
| Mahindra Bolero SLE | Mahindra | 2010 | 380000.0 | 260000.0 | Diesel | Second Owner |
| Toyota Innova 2.5 V Diesel 8-seater | Toyota | 2007 | 376412.0 | 350000.0 | Diesel | Second Owner |

## Query 12: Price Category Distribution (Dealership Tier Segmentation)

```sql
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
```

**Results (5 rows):**

| Price_Category | inventory_count | volume_pct | total_inventory_value_cr | avg_km_driven | avg_age_yrs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Mid-Range (₹3L - ₹6L) | 2637 | 38.07 | 112.71 | 74344.0 | 11.7 |
| Upper Mid-Range (₹6L - ₹10L) | 1525 | 22.02 | 112.31 | 61613.0 | 9.7 |
| Premium (₹10L - ₹20L) | 396 | 5.72 | 52.51 | 57213.0 | 9.7 |
| Budget (< ₹3L) | 2248 | 32.46 | 40.75 | 86902.0 | 16.2 |
| Luxury (> ₹20L) | 120 | 1.73 | 39.98 | 37305.0 | 9.1 |

## Query 13: Fuel Type Distribution Cross-Tabulated with Transmission

```sql
SELECT 
    Fuel_Category,
    Transmission_Category,
    COUNT(*) AS listing_count,
    ROUND(AVG(selling_price), 2) AS avg_price_inr
FROM vehicles
GROUP BY Fuel_Category, Transmission_Category
ORDER BY Fuel_Category, listing_count DESC;
```

**Results (6 rows):**

| Fuel_Category | Transmission_Category | listing_count | avg_price_inr |
| :--- | :--- | :--- | :--- |
| Cng | Manual | 56 | 300499.95 |
| Diesel | Manual | 3457 | 540677.4 |
| Diesel | Automatic | 298 | 1788778.5 |
| Lpg | Manual | 38 | 200421.05 |
| Petrol | Manual | 2791 | 331128.25 |
| Petrol | Automatic | 286 | 810545.43 |

## Query 14: Transmission Distribution Across Odometer Usage Tiers

```sql
SELECT 
    Kilometres_Category,
    Transmission_Category,
    COUNT(*) AS listing_count,
    ROUND(AVG(selling_price), 2) AS avg_price_inr
FROM vehicles
GROUP BY Kilometres_Category, Transmission_Category
ORDER BY Kilometres_Category, listing_count DESC;
```

**Results (8 rows):**

| Kilometres_Category | Transmission_Category | listing_count | avg_price_inr |
| :--- | :--- | :--- | :--- |
| High (60k - 100k km) | Manual | 2046 | 399577.17 |
| High (60k - 100k km) | Automatic | 146 | 1095383.55 |
| Low (< 30k km) | Manual | 959 | 588685.06 |
| Low (< 30k km) | Automatic | 195 | 1600015.36 |
| Moderate (30k - 60k km) | Manual | 1518 | 494484.54 |
| Moderate (30k - 60k km) | Automatic | 173 | 1369612.69 |
| Very High (> 100k km) | Manual | 1819 | 376598.87 |
| Very High (> 100k km) | Automatic | 70 | 799999.96 |

## Query 15: Brand-Wise Median Selling Price (Rank-Based Quartile Approximation)

```sql
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
```

**Results (13 rows):**

| Vehicle_Brand | brand_volume | approximate_median_price_inr |
| :--- | :--- | :--- |
| Toyota | 357 | 700000.0 |
| Honda | 362 | 560000.0 |
| Mahindra | 723 | 550000.0 |
| Ford | 361 | 450000.0 |
| Volkswagen | 174 | 422500.0 |
| Hyundai | 1267 | 412000.0 |
| Skoda | 70 | 397500.0 |
| Renault | 206 | 395000.0 |
| Nissan | 73 | 370000.0 |
| Maruti | 2165 | 350000.0 |
| Datsun | 57 | 300000.0 |
| Tata | 647 | 252999.0 |
| Chevrolet | 216 | 220000.0 |

## Query 16: Top 10 Most Expensive Vehicle Models (Minimum 10 Listings Liquidity)

```sql
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
```

**Results (10 rows):**

| Vehicle_Brand | Vehicle_Model | sample_size | avg_selling_price_inr | min_model_price_inr | max_model_price_inr |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Toyota | Fortuner 2.8 | 11 | 2908181.82 | 1500000.0 | 3200000.0 |
| Bmw | 5 Series | 12 | 2494166.67 | 890000.0 | 5200000.0 |
| Bmw | 3 Series | 14 | 1734285.71 | 480000.0 | 3200000.0 |
| Toyota | Innova Crysta | 41 | 1689341.39 | 800000.0 | 2300000.0 |
| Jeep | Compass 2.0 | 18 | 1677388.83 | 1325000.0 | 2150000.0 |
| Mercedes-Benz | New C-Class | 13 | 1270384.62 | 400000.0 | 2950000.0 |
| Mahindra | XUV500 W10 | 23 | 1241608.65 | 850000.0 | 1800000.0 |
| Mahindra | XUV500 | 14 | 1101571.29 | 850000.0 | 1500000.0 |
| Hyundai | Creta 1.6 | 58 | 1050086.17 | 700000.0 | 1950000.0 |
| Hyundai | Verna VTVT | 11 | 1024090.91 | 866000.0 | 1270000.0 |

## Query 17: Vehicle Age and Price Correlation Analysis (Price Retention by Age)

```sql
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
```

**Results (13 rows):**

| Vehicle_Age | listing_count | avg_price_inr | avg_km_driven | yoy_depreciation_pct |
| :--- | :--- | :--- | :--- | :--- |
| 6.0 | 63.0 | 888349.16 | 20641.0 |  |
| 7.0 | 347.0 | 949668.55 | 19076.0 | 6.9 |
| 8.0 | 608.0 | 866376.61 | 34938.0 | -8.77 |
| 9.0 | 808.0 | 732419.52 | 48582.0 | -15.46 |
| 10.0 | 693.0 | 653180.34 | 61230.0 | -10.82 |
| 11.0 | 681.0 | 589177.63 | 70939.0 | -9.8 |
| 12.0 | 581.0 | 511858.8 | 79416.0 | -13.12 |
| 13.0 | 562.0 | 451501.72 | 88866.0 | -11.79 |
| 14.0 | 604.0 | 351387.38 | 96478.0 | -22.17 |
| 15.0 | 554.0 | 318335.7 | 97706.0 | -9.41 |
| 16.0 | 380.0 | 273897.33 | 101862.0 | -13.96 |
| 17.0 | 240.0 | 227691.62 | 99471.0 | -16.87 |
| 18.0 | 205.0 | 208397.64 | 98479.0 | -8.47 |

## Query 18: Ownership and Price Interaction Analysis across Top 5 Brands

```sql
SELECT 
    Vehicle_Brand,
    Ownership_Category,
    COUNT(*) AS listing_count,
    ROUND(AVG(selling_price), 2) AS avg_price_inr
FROM vehicles
WHERE Vehicle_Brand IN ('Maruti', 'Hyundai', 'Mahindra', 'Tata', 'Toyota')
GROUP BY Vehicle_Brand, Ownership_Category
ORDER BY Vehicle_Brand, avg_price_inr DESC;
```

**Results (20 rows):**

| Vehicle_Brand | Ownership_Category | listing_count | avg_price_inr |
| :--- | :--- | :--- | :--- |
| Hyundai | First Owner | 770 | 538740.22 |
| Hyundai | Second Owner | 369 | 341208.58 |
| Hyundai | Third Owner | 91 | 250741.74 |
| Hyundai | Fourth & Above Owner | 37 | 214297.24 |
| Mahindra | First Owner | 452 | 701690.23 |
| Mahindra | Second Owner | 205 | 491565.8 |
| Mahindra | Third Owner | 51 | 440588.22 |
| Mahindra | Fourth & Above Owner | 15 | 357333.33 |
| Maruti | First Owner | 1298 | 468083.24 |
| Maruti | Second Owner | 612 | 293756.41 |
| Maruti | Third Owner | 188 | 220275.78 |
| Maruti | Fourth & Above Owner | 67 | 162253.72 |
| Tata | First Owner | 396 | 429434.29 |
| Tata | Second Owner | 187 | 225012.04 |
| Tata | Third Owner | 50 | 173123.48 |
| Tata | Fourth & Above Owner | 14 | 145249.93 |
| Toyota | First Owner | 196 | 1052790.76 |
| Toyota | Second Owner | 123 | 758073.11 |
| Toyota | Third Owner | 27 | 510037.0 |
| Toyota | Fourth & Above Owner | 11 | 380636.18 |

## Query 19: Seller Category and Vehicle Price Dispersion Analysis

```sql
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
```

**Results (3 rows):**

| Seller_Category | volume | min_price_inr | avg_price_inr | max_price_inr | std_dev_price_inr |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Dealer | 681 | 60000.0 | 926722.42 | 6523000.0 | 993187.6 |
| Individual | 6218 | 29999.0 | 471555.12 | 10000000.0 | 414411.07 |
| Trustmark Dealer | 27 | 225000.0 | 718111.11 | 2000000.0 | 332055.03 |

## Query 20: Comprehensive Market Segment Matrix (Fuel, Transmission, Seller)

```sql
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
```

**Results (10 rows):**

| Fuel_Category | Transmission_Category | Seller_Category | total_units | avg_price_inr | avg_km_driven |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Diesel | Manual | Individual | 3148 | 525656.54 | 93446.0 |
| Petrol | Manual | Individual | 2576 | 319810.16 | 58970.0 |
| Diesel | Manual | Dealer | 306 | 692254.85 | 67633.0 |
| Petrol | Automatic | Individual | 204 | 650495.08 | 43720.0 |
| Petrol | Manual | Dealer | 201 | 454467.59 | 39867.0 |
| Diesel | Automatic | Individual | 198 | 1498595.93 | 68108.0 |
| Diesel | Automatic | Dealer | 100 | 2363339.98 | 45705.0 |
| Petrol | Automatic | Dealer | 72 | 1267374.94 | 34494.0 |
| Cng | Manual | Individual | 56 | 300499.95 | 69329.0 |
| Lpg | Manual | Individual | 36 | 202250.0 | 91277.0 |

