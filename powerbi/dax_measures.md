# POWER BI DAX MEASURES SPECIFICATION

**Project:** Automotive Dealership Profitability & Working Capital Analysis  
**Analytical Architecture:** Star Schema Model with Financial Scenario Simulation Engine  
**Dataset Provenance:** Genuine CarDekho Used Vehicle Listing Dataset (6,926 Cleaned Vehicles)

---

## 1. Overview & Measure Governance

All DAX measures are structured under dedicated measure tables:
- `[1_Core_Market_Measures]`: Real observed marketplace listing metrics
- `[2_Scenario_Profitability_Measures]`: Unit economic simulation metrics (HYPOTHETICAL)
- `[3_Working_Capital_Measures]`: Corporate finance liquidity and CCC metrics (HYPOTHETICAL)

---

## 2. Page 1: Executive Overview Measures

### 2.1 Total Vehicle Listings
```dax
Total Vehicle Listings = 
COUNTROWS('fact_vehicles')
```
* **Format:** `#,##0`
* **Description:** Total volume of unique verified used-car listings in the dataset.

### 2.2 Total Market Listing Value
```dax
Total Listing Value INR = 
SUM('fact_vehicles'[selling_price])
```
* **Format:** `₹#,##,##0`
* **Description:** Sum of all vehicle asking prices across the portfolio.

### 2.3 Total Market Listing Value (Crores)
```dax
Total Listing Value Cr = 
DIVIDE([Total Listing Value INR], 10000000, 0)
```
* **Format:** `₹#,##0.00 "Cr"`
* **Description:** Total asking value converted to Indian Crores for high-level scorecard presentation.

### 2.4 Average Listed Selling Price
```dax
Average Selling Price = 
AVERAGE('fact_vehicles'[selling_price])
```
* **Format:** `₹#,##,##0`
* **Description:** Arithmetic mean asking price across filtered listings.

### 2.5 Median Listed Selling Price
```dax
Median Selling Price = 
MEDIAN('fact_vehicles'[selling_price])
```
* **Format:** `₹#,##,##0`
* **Description:** 50th percentile asking price, resistant to high-value luxury skew.

### 2.6 Average Kilometres Driven
```dax
Average KM Driven = 
AVERAGE('fact_vehicles'[km_driven])
```
* **Format:** `#,##0 "km"`
* **Description:** Average vehicle odometer reading.

### 2.7 Average Vehicle Age
```dax
Average Vehicle Age = 
AVERAGE('fact_vehicles'[Vehicle_Age])
```
* **Format:** `0.0 "Years"`
* **Description:** Mean vehicle age calculated from the 2026 baseline.

### 2.8 Dealer Listing Share %
```dax
Dealer Share Pct = 
DIVIDE(
    CALCULATE(
        [Total Vehicle Listings],
        'fact_vehicles'[Seller_Category] IN {"Dealer", "Trustmark Dealer"}
    ),
    [Total Vehicle Listings],
    0
)
```
* **Format:** `0.0%`
* **Description:** Percentage of listings posted by commercial dealership channels vs. individual sellers.

---

## 3. Page 2: Vehicle Profitability and Pricing Measures (Hypothetical Scenario)

> **MANDATORY AUDIT NOTICE:**  
> The measures below represent a hypothetical unit economics scenario (82% buy-in, 4% discount, ₹15,000 reconditioning, ₹5,000 transport, ₹8,000 selling costs). They do NOT reflect verified accounting records.

### 3.1 Scenario Total Revenue
```dax
Scenario Total Revenue = 
SUM('fact_profitability_scenario'[Scenario_Revenue])
```
* **Format:** `₹#,##,##0`
* **Description:** Effective simulated net revenue after anticipated negotiation markdown.

### 3.2 Scenario Total Acquisition Cost (COGS)
```dax
Scenario Acquisition Cost = 
SUM('fact_profitability_scenario'[Scenario_Acquisition_Cost])
```
* **Format:** `₹#,##,##0`
* **Description:** Assumed wholesale buy-in price (82% of list price).

### 3.3 Scenario Gross Profit
```dax
Scenario Gross Profit = 
[Scenario Total Revenue] - [Scenario Acquisition Cost]
```
* **Format:** `₹#,##,##0`
* **Description:** Scenario gross profit spread before vehicle reconditioning and direct selling costs.

### 3.4 Scenario Gross Margin %
```dax
Scenario Gross Margin Pct = 
DIVIDE([Scenario Gross Profit], [Scenario Total Revenue], 0)
```
* **Format:** `0.0%`
* **Description:** Simulated gross margin percentage (Benchmark: ~14.6%).

### 3.5 Scenario Net Contribution
```dax
Scenario Net Contribution = 
SUM('fact_profitability_scenario'[Scenario_Net_Contribution])
```
* **Format:** `₹#,##,##0`
* **Description:** Net operating contribution after deducting reconditioning (₹15k), transportation (₹5k), and selling expenses (₹8k).

### 3.6 Scenario Net Margin %
```dax
Scenario Net Margin Pct = 
DIVIDE([Scenario Net Contribution], [Scenario Total Revenue], 0)
```
* **Format:** `0.0%`
* **Description:** Scenario net profit margin after all direct unit refurbishment and selling expenses.

---

## 4. Page 3: Inventory and Vehicle Analysis Measures

### 4.1 Top 3 Brand Concentration %
```dax
Top 3 Brand Concentration Pct = 
VAR Top3Volume = 
    CALCULATE(
        [Total Vehicle Listings],
        TOPN(3, ALLSELECTED('dim_brand'), [Total Vehicle Listings], DESC)
    )
RETURN
    DIVIDE(Top3Volume, [Total Vehicle Listings], 0)
```
* **Format:** `0.0%`
* **Description:** Share of total vehicle listings concentrated in the top 3 manufacturers (Maruti, Hyundai, Mahindra).

### 4.2 Diesel Volume Share %
```dax
Diesel Share Pct = 
DIVIDE(
    CALCULATE([Total Vehicle Listings], 'fact_vehicles'[Fuel_Category] = "Diesel"),
    [Total Vehicle Listings],
    0
)
```
* **Format:** `0.0%`
* **Description:** Percentage of listings powered by diesel engines.

### 4.3 High-Mileage Vehicle Proportion
```dax
High Mileage Vehicle Pct = 
DIVIDE(
    CALCULATE([Total Vehicle Listings], 'fact_vehicles'[km_driven] > 100000),
    [Total Vehicle Listings],
    0
)
```
* **Format:** `0.0%`
* **Description:** Proportion of vehicles with odometer readings exceeding 100,000 km.

---

## 5. Page 4: Working Capital Scenario Measures (Hypothetical)

### 5.1 Net Working Capital (INR)
```dax
NWC Amount INR = 
SELECTEDVALUE('fact_working_capital_scenarios'[Net Working Capital (₹ Cr)]) * 10000000
```
* **Format:** `₹#,##0.00 "Cr"`
* **Description:** Current Assets minus Current Liabilities for the active scenario.

### 5.2 Current Ratio
```dax
Current Ratio Measure = 
SELECTEDVALUE('fact_working_capital_scenarios'[Current Ratio])
```
* **Format:** `0.00"x"`
* **Description:** Coverage multiple of short-term obligations by short-term assets.

### 5.3 Quick Ratio (Acid-Test)
```dax
Quick Ratio Measure = 
SELECTEDVALUE('fact_working_capital_scenarios'[Quick Ratio])
```
* **Format:** `0.00"x"`
* **Description:** Immediate liquidity coverage excluding slow-moving lot inventory.

### 5.4 Days Sales of Inventory (DSI / DIO)
```dax
Days Sales Inventory = 
SELECTEDVALUE('fact_working_capital_scenarios'[Inventory Days (DSI)])
```
* **Format:** `0.0 "days"`
* **Description:** Average vehicle lot turn time before retail delivery.

### 5.5 Days Sales Outstanding (DSO)
```dax
Days Sales Outstanding = 
SELECTEDVALUE('fact_working_capital_scenarios'[DSO (Days)])
```
* **Format:** `0.0 "days"`
* **Description:** Debtor lag for finance payouts and trade credit.

### 5.6 Days Payable Outstanding (DPO)
```dax
Days Payable Outstanding = 
SELECTEDVALUE('fact_working_capital_scenarios'[DPO (Days)])
```
* **Format:** `0.0 "days"`
* **Description:** Supplier credit term extended by wholesale sources.

### 5.7 Cash Conversion Cycle (CCC)
```dax
Cash Conversion Cycle Days = 
SELECTEDVALUE('fact_working_capital_scenarios'[Cash Conversion Cycle (Days)])
```
* **Format:** `0.0 "days"`
* **Description:** Comprehensive operating cycle: `DSI + DSO - DPO`.

---

## 6. Page 5: Financial Scenario and Management Insights Measures

### 6.1 Working Capital Interest Drag
```dax
WC Floorplan Interest Drag INR = 
SELECTEDVALUE('fact_working_capital_scenarios'[Carrying Cost @ 10.5% (₹ Lakhs)]) * 100000
```
* **Format:** `₹#,##0.0 "L"`
* **Description:** Annual floor-plan carrying burden on idle lot inventory.

### 6.2 Scenario Working Capital Liberation (Lean vs. Base)
```dax
WC Capital Liberation Cr = 
VAR BaseNWC = CALCULATE(MAX('fact_working_capital_scenarios'[Net Working Capital (₹ Cr)]), 'fact_working_capital_scenarios'[Scenario] = "Base Case (Standard Dealership)")
VAR LeanNWC = CALCULATE(MAX('fact_working_capital_scenarios'[Net Working Capital (₹ Cr)]), 'fact_working_capital_scenarios'[Scenario] = "Lean Optimized (Fast Velocity)")
RETURN
    BaseNWC - LeanNWC
```
* **Format:** `₹#,##0.00 "Cr"`
* **Description:** Cash liberated by transitioning from traditional inventory velocity to lean inventory turn.
