# POWER BI DASHBOARD IMPLEMENTATION & SETUP GUIDE

**Project:** Automotive Dealership Profitability & Working Capital Analysis  
**Author:** Senior Financial Analyst & Power BI Developer  
**Dataset:** Real CarDekho Vehicle Listings (6,926 Unique Processed Records)

---

## 1. Quick Start Checklist

1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Navigate to `powerbi/data/` and import the following 5 CSV files:
   - `fact_vehicles.csv`
   - `fact_profitability_scenario.csv`
   - `fact_working_capital_scenarios.csv`
   - `dim_brand.csv`
   - `dim_price_tier.csv`
4. Confirm data types and relationship connections per `powerbi/data_model.md`.
5. Create a dedicated Measure Table `_Key_Measures` and copy DAX definitions from `powerbi/dax_measures.md`.

---

## 2. Visual Palette & Brand Identity

- **Primary Corporate Navy:** `#1B365D`
- **Secondary Slate:** `#2C3E50`
- **Accent Blue:** `#2A6F97`
- **Profit / Green:** `#27AE60`
- **Warning / Amber:** `#E67E22`
- **Alert / Red:** `#C0392B`
- **Background:** `#F8F9FA` / `#FFFFFF`
- **Canvas Dimensions:** 16:9 Standard (1280 x 720 px)

---

## 3. Five-Page Dashboard Specification

### PAGE 1: EXECUTIVE OVERVIEW
- **Header:** Automotive Dealership Portfolio Overview | 2026 Baseline
- **Top KPI Cards (5):**
  1. `[Total Vehicle Listings]` (6,926)
  2. `[Average Selling Price]` (₹5.97 Lakhs)
  3. `[Median Selling Price]` (₹4.50 Lakhs)
  4. `[Average Vehicle Age]` (12.2 Years)
  5. `[Average KM Driven]` (69,820 km)
- **Visual 1 (Horizontal Bar):** Vehicle Distribution by Brand (Top 10 Volume - Maruti, Hyundai, Mahindra leading)
- **Visual 2 (Histogram / Area):** Listed Selling Price Distribution (Concentration between ₹2L and ₹8L)
- **Visual 3 (Donut Chart):** Listings Share by Fuel Type (Diesel 54%, Petrol 45%)
- **Visual 4 (Stacked Bar):** Dealer vs Individual Seller Volume Distribution
- **Slicers:** Vehicle Brand, Fuel Category, Transmission, Year Range Slider

---

### PAGE 2: VEHICLE PROFITABILITY AND PRICING
- **Header:** Vehicle Profitability & Unit Economics (Hypothetical Financial Model)
- **Top Audit Banner:** `HYPOTHETICAL FINANCIAL SCENARIO – NOT ACTUAL DEALERSHIP ACCOUNTING DATA`
- **Visual 1 (Clustered Column):** Top 10 Brands: Scenario Revenue vs Scenario Gross Profit
- **Visual 2 (Line Chart):** Scenario Gross Margin % across Price Categories (Budget to Luxury)
- **Visual 3 (Matrix / Table):** Brand-Level Economics:
  - Rows: `Vehicle_Brand`
  - Columns: `Listing Count`, `Avg Asking Price`, `Scenario Gross Profit`, `Scenario Gross Margin %`, `Scenario Net Contribution`
- **Visual 4 (Scatter Plot):** Asking Price vs Scenario Net Contribution Margin %
- **Slicers:** Price Category, Fuel Type, Ownership Tier

---

### PAGE 3: INVENTORY AND VEHICLE ANALYSIS
- **Header:** Used Vehicle Inventory Composition & Liquidity Characteristics
- **Visual 1 (Column Chart):** Vehicle Age Distribution (Cohort buckets: Under 7 Yrs, 7-10 Yrs, 11-15 Yrs, Over 15 Yrs)
- **Visual 2 (Box Plot / Violin):** Kilometres Driven Distribution across Fuel Types
- **Visual 3 (Treemap):** Brand Market Value Concentration (Market Capitalization of Listings)
- **Visual 4 (Donut Chart):** Ownership History Distribution (1st Owner, 2nd Owner, 3rd Owner, 4th & Above)
- **Visual 5 (Table):** Most Prevalent Vehicle Models (Volume, Avg Price, Median Age, Odometer)
- **Footnote:** All metrics reflect public listings, not verified dealer stockholding turn.

---

### PAGE 4: WORKING CAPITAL SCENARIO
- **Header:** Corporate Finance Working Capital & Liquidity Simulation
- **Top Audit Banner:** `ILLUSTRATIVE WORKING CAPITAL MODEL – USER-ENTERED ASSUMPTIONS`
- **Scenario Slicer (Single Select):**
  - Base Case (Standard Dealership)
  - Lean Optimized (Fast Velocity)
  - Stressed (High Lot Aging)
- **KPI Cards (4):**
  1. `[Net Working Capital]`
  2. `[Current Ratio]` (Benchmark: 1.30x - 1.50x)
  3. `[Quick Ratio]` (Benchmark: > 1.00x)
  4. `[Cash Conversion Cycle]` (CCC Days)
- **Visual 1 (Waterfall / Clustered Bar):** Operating Cycle Breakdown (`DSI` + `DSO` - `DPO` = `CCC`)
- **Visual 2 (Gauge / Bullet Chart):** Current Ratio vs Target Thresholds
- **Visual 3 (Bar Chart):** Annual Floor-plan Capital Carrying Drag across Scenarios (₹ Lakhs)

---

### PAGE 5: FINANCIAL SCENARIO AND MANAGEMENT INSIGHTS
- **Header:** Financial Scenario Comparison & Strategic Recommendations
- **Visual 1 (Comparison Matrix):** Side-by-Side Scenario Performance (Base vs Lean vs Stressed)
  - Dimensions: Current Assets, Current Liabilities, NWC, Current Ratio, DSI, DSO, DPO, CCC, Carrying Cost
- **Visual 2 (Card Callout):** `[WC Capital Liberation Cr]` (Capital freed by switching to Lean Turn)
- **Visual 3 (Executive Narrative Card):**
  - Action 1: Enforce 45-day lot aging limit to prevent valuation erosion and floor-plan interest accumulation.
  - Action 2: Prioritize high-liquidity models (Maruti Swift, Dzire, Hyundai i20) with proven sub-30-day velocity.
  - Action 3: Streamline retail finance approvals to compress DSO from 20 days to 12 days.
  - Action 4: Negotiate wholesale vendor trade terms to stretch DPO towards 40 days.
