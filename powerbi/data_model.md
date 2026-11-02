# POWER BI DATA MODEL ARCHITECTURE

**Project:** Automotive Dealership Profitability & Working Capital Analysis  
**Model Design:** Hybrid Star / Analytical Schema  
**Target Environment:** Power BI Desktop / Power BI Service  

---

## 1. Entity-Relationship Overview

```
                      +-------------------+
                      |     dim_brand     |
                      +-------------------+
                                | (1)
                                |
                                | (*)
                      +-------------------+
                      |   fact_vehicles   | <------- (1) [dim_price_tier]
                      +-------------------+
                                | (1)
                                |
                                | (1)
                      +-------------------------------+
                      |  fact_profitability_scenario  |
                      +-------------------------------+

                      +-----------------------------------+
                      |  fact_working_capital_scenarios   | (Disconnected Parameter)
                      +-----------------------------------+
```

---

## 2. Table Specifications

### 2.1 `fact_vehicles` (Central Market Observations)
- **Source File:** `powerbi/data/fact_vehicles.csv`
- **Grain:** One row per verified unique vehicle listing (6,926 records)
- **Primary Key:** `name` + `year` + `selling_price` + `km_driven` (Composite / Auto-generated ID)
- **Key Columns & Data Types:**
  - `name` (Text): Vehicle listing title
  - `year` (Integer): Model year
  - `selling_price` (Decimal Currency): Listed asking price (INR)
  - `km_driven` (Decimal / Integer): Odometer reading
  - `fuel` (Text): Standardized fuel category
  - `seller_type` (Text): Channel (Dealer / Trustmark Dealer / Individual)
  - `transmission` (Text): Manual / Automatic
  - `owner` (Text): Ownership history tier
  - `Vehicle_Brand` (Text): Manufacturer OEM
  - `Vehicle_Model` (Text): Model line
  - `Vehicle_Age` (Integer): Years from 2026 baseline
  - `Price_Category` (Text): Tier (Budget, Mid-Range, Upper Mid-Range, Premium, Luxury)
  - `Mileage_kmpl` (Decimal): Fuel efficiency rating

### 2.2 `fact_profitability_scenario` (Unit Economics Simulation)
- **Source File:** `powerbi/data/fact_profitability_scenario.csv`
- **Grain:** One row per vehicle listing with simulated financials (6,926 records)
- **Relationship to `fact_vehicles`:** 1-to-1 matching row index
- **Key Fields:**
  - `Scenario_Expected_Selling_Price` (Decimal)
  - `Scenario_Discount` (Decimal)
  - `Scenario_Revenue` (Decimal)
  - `Scenario_Acquisition_Cost` (Decimal)
  - `Scenario_Gross_Profit` (Decimal)
  - `Scenario_Gross_Margin_Pct` (Decimal)
  - `Scenario_Reconditioning_Cost` (Decimal)
  - `Scenario_Transportation_Cost` (Decimal)
  - `Scenario_Other_Selling_Costs` (Decimal)
  - `Scenario_Net_Contribution` (Decimal)
  - `Scenario_Net_Margin_Pct` (Decimal)
  - `Scenario_Data_Classification` (Text): `HYPOTHETICAL FINANCIAL SCENARIO`

### 2.3 `fact_working_capital_scenarios` (Corporate Finance Benchmarks)
- **Source File:** `powerbi/data/fact_working_capital_scenarios.csv`
- **Grain:** One row per benchmark scenario (3 records: Base Case, Lean Optimized, Stressed)
- **Usage:** Disconnected parameter table for scenario slicing and executive benchmarking.
- **Key Fields:**
  - `Scenario` (Text)
  - `Current Assets (₹ Cr)` (Decimal)
  - `Current Liabilities (₹ Cr)` (Decimal)
  - `Net Working Capital (₹ Cr)` (Decimal)
  - `Current Ratio` (Decimal)
  - `Quick Ratio` (Decimal)
  - `Inventory Turnover (x)` (Decimal)
  - `Inventory Days (DSI)` (Decimal)
  - `DSO (Days)` (Decimal)
  - `DPO (Days)` (Decimal)
  - `Cash Conversion Cycle (Days)` (Decimal)
  - `Carrying Cost @ 10.5% (₹ Lakhs)` (Decimal)

### 2.4 `dim_brand` (Manufacturer Master)
- **Source File:** `powerbi/data/dim_brand.csv`
- **Grain:** One row per brand (32 automotive manufacturers)
- **Relationship:** 1-to-many with `fact_vehicles[Vehicle_Brand]`
- **Filter Direction:** Single (dim_brand filters fact_vehicles)

### 2.5 `dim_price_tier` (Price Tier Master)
- **Source File:** `powerbi/data/dim_price_tier.csv`
- **Grain:** 5 price brackets (Budget to Luxury)
- **Relationship:** 1-to-many with `fact_vehicles[Price_Category]`

---

## 3. Relationships & Model Properties

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter | Active |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `dim_brand` | `Vehicle_Brand` | `fact_vehicles` | `Vehicle_Brand` | 1:* | Single | Yes |
| `dim_price_tier` | `Price_Category` | `fact_vehicles` | `Price_Category` | 1:* | Single | Yes |
| `fact_vehicles` | `row_id` | `fact_profitability_scenario` | `row_id` | 1:1 | Both | Yes |
