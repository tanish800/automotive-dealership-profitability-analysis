# Automotive Dealership Profitability & Working Capital Analysis

[![Python 3.13](https://img.shields.io/badge/Python-3.13.1-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: Pytest](https://img.shields.io/badge/Pytest-16%20Passed-brightgreen.svg)](https://pytest.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App%20Live-FF4B4B.svg)](https://streamlit.io/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Model%20Ready-F2C811.svg)](https://powerbi.microsoft.com/)
[![Excel](https://img.shields.io/badge/Excel-11%20Sheets-217346.svg)](https://microsoft.com/excel)
[![SQLite](https://img.shields.io/badge/SQLite-20%20Queries-003B57.svg)](https://sqlite.org/)

An institutional-grade, end-to-end financial analytics, valuation, and working capital intelligence project built on a **single real-world public dataset**. Designed for finance professionals and B.Com + MBA Finance candidates targeting roles in:
- **Financial Analyst / Finance Analyst**
- **Business Analyst & Commercial Finance**
- **Financial Planning & Analysis (FP&A)**
- **MIS & Corporate Reporting**
- **Business Operations & Automotive Consulting**

---

## MANDATORY REGULATORY & AUDIT GOVERNANCE NOTICE

> **AUDIT CLASSIFICATION: DUAL-TIER ANALYTICAL ARCHITECTURE**  
> 1. **Empirical Public Dataset:** All vehicle listing counts, asking prices, odometer readings, manufacturing years, fuel types, transmission shares, and ownership records are derived exclusively from the genuine **CarDekho Vehicle Dataset** sourced from Kaggle.  
> 2. **Hypothetical Financial Modeling:** Because the public dataset contains marketplace asking prices and physical vehicle attributes—and **does NOT contain dealership wholesale buy-in invoices, dealer accounting ledgers, accounts receivable, trade payables, or cash balances**—all unit gross profit spreads, net contributions, and working capital cash conversion cycles are derived from **explicit corporate finance scenario simulation models**.  
> 3. **Zero Synthetic Records:** No fake dealership sales ledgers, artificial transaction histories, or fabricated accounting datasets were mixed with or substituted for the real dataset.

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Business Problem & Strategic Context](#2-business-problem--strategic-context)
3. [Project Objectives](#3-project-objectives)
4. [Real Dataset Provenance & Attribution](#4-real-dataset-provenance--attribution)
5. [Data Cleaning & Feature Engineering Methodology](#5-data-cleaning--feature-engineering-methodology)
6. [Financial Methodology & KPI Formulations](#6-financial-methodology--kpi-formulations)
7. [Repository Architecture](#7-repository-architecture)
8. [Advanced Excel Financial Workbook (11 Worksheets)](#8-advanced-excel-financial-workbook-11-worksheets)
9. [Power BI Dashboard Architecture (5 Pages)](#9-power-bi-dashboard-architecture-5-pages)
10. [Interactive Streamlit Financial Application (7 Modules)](#10-interactive-streamlit-financial-application-7-modules)
11. [SQL Business Analytics (20 Queries)](#11-sql-business-analytics-20-queries)
12. [Visual Analytics & Charts](#12-visual-analytics--charts)
13. [Key Business Findings & Insights](#13-key-business-findings--insights)
14. [Limitations & Methodological Boundaries](#14-limitations--methodological-boundaries)
15. [Future Scope](#15-future-scope)
16. [Installation & Execution Guide](#16-installation--execution-guide)
17. [GitHub Deployment Commands](#17-github-deployment-commands)
18. [Verification Checklist](#18-verification-checklist)

---

## 1. Project Overview

Pre-owned automotive retail is a high-volume, working-capital-intensive industry characterized by rapid vehicle depreciation, localized pricing dispersion, and substantial carrying costs. Dealership profitability is determined not merely by headline selling prices, but by **inventory turn velocity**, **reconditioning cost control**, and **working capital efficiency**.

This project establishes a complete analytics ecosystem that:
- Ingests and cleans **6,926 unique real-world used-car listings** representing **₹413.4 Crores** in marketplace asking value across **32 automotive brands**.
- Simulates unit economics across budget, mid-range, upper-mid, premium, and luxury vehicle tiers under configurable buy-in and refurbishment assumptions.
- Models corporate working capital liquidity (Current Ratio, Quick Ratio, Inventory Turnover, DSI, DSO, DPO, Cash Conversion Cycle, and Floor-Plan Carrying Drag) across three standardized industry operating benchmarks.
- Deploys multi-platform deliverables: an 11-worksheet openpyxl financial Excel model, a 5-page Power BI data model with 25+ DAX measures, a 20-query SQLite analytical database, an interactive 7-page Streamlit portal, and publication-ready Markdown/PDF executive reports.

---

## 2. Business Problem & Strategic Context

Automotive dealership leadership faces three acute operational and financial challenges:
1. **Margin Compression from Hidden Lot Aging:** Vehicles parked on dealership lots beyond 45 days suffer severe visual and mechanical depreciation, forcing emergency price markdowns that erode gross margins.
2. **Floor-Plan Borrowing Interest Drag:** Unsold vehicle inventory is typically financed through revolving short-term credit lines (floor-plan debt) at 10%–12% annual interest. Sluggish inventory turnover directly inflates financing interest expenses.
3. **Cash Conversion Cycle Bottlenecks:** Delays in customer auto loan disbursals (inflated DSO) combined with compressed vendor trade terms (compressed DPO) trap liquidity in working capital, restricting a dealer's capacity to acquire high-demand, high-turn trade-in stock.

---

## 3. Project Objectives

- **Empirical Market Baseline:** Measure real vehicle pricing distributions, brand concentration, odometer usage, and depreciation profiles across 6,926 verified listings.
- **Parametric Unit Economics Modeling:** Construct a flexible simulation engine calculating Scenario Revenue, Gross Profit, Gross Margin %, Reconditioning Burden, and Net Contribution Margin %.
- **Corporate Working Capital Optimization:** Quantify the cash flow liberation achieved by transitioning from traditional inventory holding (67 days DSI) to lean fast-turn operations (39 days DSI).
- **Institutional Portfolio Artifacts:** Provide production-ready assets suitable for a Senior Financial Analyst or FP&A professional portfolio.

---

## 4. Real Dataset Provenance & Attribution

- **Dataset Name:** Vehicle Dataset from CarDekho
- **Curator:** Nehal Birla
- **Platform:** Kaggle
- **Source Link:** [https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho)
- **License:** CC0: Public Domain / Open Database License
- **Storage:** Pristine raw dataset stored in `data/raw/Car details v3.csv` (8,128 rows) and `data/raw/CAR DETAILS FROM CAR DEKHO.csv` (4,340 rows).
- **Native Columns:** `name`, `year`, `selling_price`, `km_driven`, `fuel`, `seller_type`, `transmission`, `owner`, `mileage`, `engine`, `max_power`, `torque`, `seats`.

---

## 5. Data Cleaning & Feature Engineering Methodology

The raw dataset was cleaned using Python (`pandas`, `numpy`, `re`) via `src/data_cleaning.py`:

```
Raw Listings (8,128 rows)
      │
      ▼
1. Deduplication (Eliminated 1,202 duplicate re-posts)
      │
      ▼
2. Cleaned Unique Population (6,926 verified unique listings)
      │
      ▼
3. Brand & Model Parsing (Extracted OEM Brand & Model lines, e.g. Land Rover, Ashok Leyland)
      │
      ▼
4. Temporal Anchoring (Vehicle_Age = 2026 - year; baseline November 2026)
      │
      ▼
5. Specification Standardization (Mileage_kmpl, Engine_cc, Max_Power_bhp extracted as numeric floats)
      │
      ▼
6. Outlier Auditing (Flagged via 1.5 * IQR Fence without arbitrary data destruction)
      │
      ▼
7. Feature Engineering (Price_Category, Kilometres_Category, Vehicle_Age_Group, Mileage_Category)
      │
      ▼
Cleaned Dataset Exported: data/processed/cleaned_vehicle_data.csv (6,926 rows, 30 columns)
```

---

## 6. Financial Methodology & KPI Formulations

### 6.1 Unit Economics Simulation (Hypothetical)
- **Scenario Revenue:** $\text{Expected Selling Price} \times (1 - \text{Discount Rate})$ (Default Discount = 4%)
- **Scenario Acquisition Cost (COGS):** $\text{Expected Selling Price} \times \text{Acquisition Rate}$ (Default Buy-in = 82%)
- **Scenario Gross Profit:** $\text{Scenario Revenue} - \text{Scenario Acquisition Cost}$
- **Scenario Gross Margin %:** $(\text{Scenario Gross Profit} / \text{Scenario Revenue}) \times 100$
- **Scenario Direct Costs:** Reconditioning (₹15,000) + Transport (₹5,000) + Selling Expenses (₹8,000) = ₹28,000
- **Scenario Net Contribution:** $\text{Scenario Gross Profit} - \text{Scenario Direct Costs}$
- **Scenario Net Margin %:** $(\text{Scenario Net Contribution} / \text{Scenario Revenue}) \times 100$

### 6.2 Working Capital Scenario Formulations (Hypothetical)
- **Net Working Capital (NWC):** $\text{Current Assets} - \text{Current Liabilities}$
- **Current Ratio:** $\text{Current Assets} / \text{Current Liabilities}$ (Benchmark: 1.30x–1.50x)
- **Quick Ratio:** $(\text{Current Assets} - \text{Inventory}) / \text{Current Liabilities}$ (Benchmark: > 0.60x)
- **Inventory Turnover:** $\text{Annual COGS} / \text{Average Inventory}$
- **Days Sales of Inventory (DSI):** $(\text{Average Inventory} / \text{Annual COGS}) \times 365$
- **Days Sales Outstanding (DSO):** $(\text{Average Accounts Receivable} / \text{Annual Credit Sales}) \times 365$
- **Days Payable Outstanding (DPO):** $(\text{Average Accounts Payable} / \text{Annual Credit Purchases}) \times 365$
- **Cash Conversion Cycle (CCC):** $\text{DSI} + \text{DSO} - \text{DPO}$
- **Annual Floor-Plan Carrying Drag:** $\text{NWC} \times \text{Cost of Debt (10.5\%)}$

---

## 7. Repository Architecture

```
automotive-dealership-profitability-analysis/
├── data/
│   ├── raw/
│   │   ├── Car details v3.csv              # Genuine Kaggle raw dataset (8,128 rows)
│   │   ├── CAR DETAILS FROM CAR DEKHO.csv  # 8-column raw dataset (4,340 rows)
│   │   ├── car data.csv                    # 301-row sample
│   │   └── car details v4.csv              # Alternate schema
│   └── processed/
│       └── cleaned_vehicle_data.csv        # Cleaned unique population (6,926 rows, 30 cols)
│
├── notebooks/
│   └── exploratory_analysis.ipynb          # Jupyter Notebook with EDA and modeling walkthrough
│
├── src/
│   ├── data_loader.py                      # Provenance tracking and raw dataset ingestion
│   ├── data_cleaning.py                    # 10-step cleaning, deduplication, feature derivation
│   ├── vehicle_analysis.py                 # Market distribution, EDA, and 9 matplotlib figures
│   ├── profitability_scenario.py           # Parametric unit economics simulation engine
│   ├── working_capital.py                  # Corporate finance working capital and CCC model
│   ├── excel_generator.py                  # 11-sheet openpyxl institutional workbook generator
│   └── report_generator.py                 # Markdown and ReportLab PDF report compiler
│
├── sql/
│   ├── database_schema.sql                 # SQLite schema with analytics indexes
│   ├── dealership.db                       # Ingested SQLite database (6,926 records)
│   ├── analysis_queries.sql                # 20 complete business SQL queries
│   ├── run_queries.py                      # Automated query executor and markdown formatter
│   └── query_results.md                    # Formatted query outputs and result tables
│
├── excel/
│   └── Automotive_Dealership_Analysis.xlsx # 11-worksheet financial model with native formulas & charts
│
├── powerbi/
│   ├── dax_measures.md                     # 25+ production DAX measures with exact formulas
│   ├── data_model.md                       # Star schema documentation & ER diagram
│   ├── setup_guide.md                      # Step-by-step visual dashboard layout guide
│   ├── prepare_powerbi_data.py             # Export script for Power BI dimension/fact tables
│   └── data/                               # Pre-exported CSV tables for Power BI import
│       ├── fact_vehicles.csv
│       ├── fact_profitability_scenario.csv
│       ├── fact_working_capital_scenarios.csv
│       ├── dim_brand.csv
│       └── dim_price_tier.csv
│
├── dashboard/
│   └── app.py                              # 7-page interactive Streamlit web application
│
├── outputs/
│   ├── charts/                             # 11 high-resolution visual analytics charts (.png)
│   └── reports/                            # Comprehensive data quality, SQL, and executive reports
│       ├── data_quality_report.json
│       ├── data_quality_report.md
│       ├── market_analysis_summary.json
│       ├── profitability_scenario_summary.json
│       ├── working_capital_summary.json
│       ├── sql_analysis_summary.md
│       ├── Management_Financial_Report.md  # 14-section institutional management report
│       └── Management_Financial_Report.pdf # Publication-ready compiled PDF
│
├── tests/
│   └── test_analysis.py                    # Automated pytest suite (16 tests, 100% pass)
│
├── docs/
│   ├── dataset_documentation.md            # Data provenance, dictionary, and cleaning audit
│   ├── financial_methodology.md            # Formulas, mathematical definitions, and benchmarks
│   └── limitations.md                      # Transparent methodological boundaries & disclaimers
│
├── requirements.txt                        # Pinned dependencies
├── README.md                               # Comprehensive documentation
├── LICENSE                                 # MIT License
└── .gitignore                              # Production git exclusions
```

---

## 8. Advanced Excel Financial Workbook (11 Worksheets)

The workbook `excel/Automotive_Dealership_Analysis.xlsx` was generated programmatically using `openpyxl`:

1. **`Executive_Summary`:** Strategic KPI tiles, executive scorecards, workbook navigation matrix, and mandatory audit disclaimers.
2. **`Raw_Data`:** First 500 records of unchanged raw data for audit verification.
3. **`Cleaned_Data`:** Full 6,926-vehicle cleaned analytical population with derived dimensions.
4. **`Vehicle_Analysis`:** Vehicle age cohort distribution, odometer tiers, and native column chart.
5. **`Brand_Analysis`:** Top 15 brands summary with volume, market share %, market value (₹ Cr), average price, and bar chart.
6. **`Pricing_Analysis`:** Five price tiers (Budget to Luxury) with volume share, value share, and pie chart.
7. **`Fuel_Analysis`:** Diesel vs. Petrol vs. CNG vs. LPG metrics and Transmission price premium cross-tab.
8. **`Ownership_Analysis`:** 1st, 2nd, 3rd, 4th owner valuation discount calculations relative to first owners.
9. **`Profitability_Scenario`:** Dynamic assumption cells (Acquisition Cost %, Discount %, Reconditioning, Transport, Selling Expenses) driving 500 rows of live formula-based vehicle unit economics.
10. **`Working_Capital_Model`:** Corporate finance calculator with dynamic balance sheet inputs, live ratio formulas, 3-scenario comparison table, and conditional formatting on CCC.
11. **`Financial_KPI_Dashboard`:** Executive scorecard linking to all underlying worksheets via native `=Sheet!Cell` references.

---

## 9. Power BI Dashboard Architecture (5 Pages)

Full details in `powerbi/setup_guide.md` and `powerbi/dax_measures.md`:

- **Page 1: Executive Overview:** Total Listings (6,926), Avg Asking Price (₹5.97L), Median Price (₹4.50L), Avg Age (12.2 Yrs), Avg KM (69,820 km), Brand distribution, and Fuel/Transmission share.
- **Page 2: Vehicle Profitability & Pricing:** Clustered bar charts of Scenario Gross Profit and Net Contribution, Gross Margin % across price tiers, and scatter plot of price vs. net margin.
- **Page 3: Inventory & Vehicle Analysis:** Vehicle age cohort breakdown, odometer violin plots, brand market capitalization treemap, and ownership history donut chart.
- **Page 4: Working Capital Scenario:** Dynamic scenario slicer (Base Case vs. Lean Optimized vs. Stressed), Current Ratio gauge, Quick Ratio card, and CCC waterfall chart.
- **Page 5: Financial Scenario & Management Insights:** Scenario comparison matrix, capital liberation callout (₹1.30 Cr freed in Lean Turn), and strategic action narrative cards.

---

## 10. Interactive Streamlit Financial Application (7 Modules)

Launch via `streamlit run dashboard/app.py`:

1. **🏢 Executive Dashboard:** Dynamic KPI cards, top brands bar chart, price distribution histogram, fuel donut chart, and seller channel comparison.
2. **🚗 Vehicle Market Analysis:** Age depreciation curves, odometer vs. price regression scatter plot, and ownership valuation discount table.
3. **🏷️ Brand & Model Analytics:** Manufacturer mean vs. median price comparisons and top 15 most liquid vehicle model lines.
4. **💰 Pricing & Valuation:** Capital allocation pie chart and price tier segmentation table.
5. **📈 Profitability Scenario Calculator:** Real-time sliders for acquisition %, discount %, reconditioning, transport, and selling expenses with instant portfolio recalculation and waterfall charts.
6. **💼 Working Capital Calculator:** Interactive balance sheet inputs, one-click preset buttons (Base, Lean, Stressed), liquidity ratios, and CCC breakdown.
7. **📄 Reports & Downloads:** Direct download buttons for Cleaned CSV, Excel Workbook, SQL Report, and in-app markdown report viewer.

---

## 11. SQL Business Analytics (20 Queries)

All queries are persisted in `sql/analysis_queries.sql` and executed on `sql/dealership.db`:

1. Average selling price by brand (ranked by listing volume).
2. Top 10 highest-priced vehicles in marketplace.
3. Top 10 lowest-priced (liquidation) vehicles.
4. Average price and fuel efficiency by fuel type.
5. Valuation premium of Automatic vs. Manual transmission.
6. Average price and discount across ownership categories.
7. Dealer vs. individual listing channel comparison.
8. Brand-wise volume distribution and cumulative concentration.
9. Vehicle age cohort analysis (volume and odometer by age bracket).
10. Price distribution by manufacturing year (depreciation curve).
11. Top 10 highest-mileage vehicles (fleet road warriors).
12. Price category distribution and inventory capital value.
13. Fuel type distribution cross-tabulated with transmission.
14. Transmission distribution across odometer usage tiers.
15. Brand-wise approximate median selling price using window functions.
16. Top 10 most expensive vehicle models (minimum 10 listings liquidity).
17. Vehicle age YoY price depreciation correlation analysis.
18. Ownership and price interaction across the top 5 brands.
19. Seller category price dispersion and standard deviation.
20. Comprehensive market segment matrix (Fuel, Transmission, Seller).

---

## 12. Visual Analytics & Charts

All high-resolution figures are generated in `outputs/charts/`:

| Chart File | Visual Dimension & Description |
| :--- | :--- |
| `brand_distribution.png` | Market Concentration: Top 10 Automotive Brands by Volume |
| `selling_price_distribution.png` | Histogram and KDE of Vehicle Asking Prices (₹ Lakhs) |
| `fuel_and_transmission_distribution.png` | Listing Volume Share by Fuel Type & Transmission |
| `brand_pricing_analysis.png` | Mean vs. Median Asking Prices for Top 12 Brands |
| `age_depreciation_curve.png` | Depreciation Curve: Selling Price vs. Vehicle Age (2026 Baseline) |
| `km_vs_price_scatter.png` | Odometer Utilization vs. Valuation with Regression Trendline |
| `dealer_vs_individual_comparison.png` | Listing Price Dispersion: Dealer vs. Individual Channels |
| `ownership_pricing_impact.png` | Valuation Discount Across Ownership Tiers |
| `price_category_segmentation.png` | Market Volume Breakdown across 5 Price Categories |
| `scenario_profitability_analysis.png` | Brand Scenario Gross Profit vs. Net Contribution |
| `working_capital_analysis.png` | Cash Conversion Cycle Breakdown & Liquidity Ratios across Scenarios |

---

## 13. Key Business Findings & Insights

1. **Market Oligopoly Concentration:** The top 3 OEM manufacturers—**Maruti Suzuki (31.3%)**, **Hyundai (18.3%)**, and **Mahindra (10.4%)**—capture **60.0% of total marketplace listings**. Sourcing strategies must align with these high-turnover brands to maintain lot liquidity.
2. **Significant Right-Skewed Pricing:** The mean asking price (₹5.97 Lakhs) exceeds the median (₹4.50 Lakhs) by **32.7%**, driven by luxury exotics (BMW, Mercedes-Benz, Land Rover).
3. **Diesel Value Premium:** Diesel vehicles account for **54.3% of listings** and average **₹6.70 Lakhs**, commanding a substantial price premium over petrol vehicles (₹4.95 Lakhs) due to SUV popularity.
4. **Ownership Valuation Erosion:** Relative to First Owner vehicles, Second Owner listings trade at a **~25% discount**, Third Owners at **~40% discount**, and Fourth & Above at **~55% discount**.
5. **Working Capital Transformation:** Under standard dealership operations, capital is locked for **54.2 days**. Transitioning to a Lean Optimized inventory turn compresses holding days from 67 to 39, liberating **₹1.30 Crores in liquid working capital** and reducing the Cash Conversion Cycle to **8.7 days**.

---

## 14. Limitations & Methodological Boundaries

- **Asking Prices vs. Final Invoice Prices:** Dataset reflects public listing prices. A 4% negotiation buffer was applied in scenarios to approximate net realized revenue.
- **Absence of Dealer COGS:** The real dataset contains no wholesale buy-in costs. Gross profit and margins are simulated via parametric scenario models.
- **Cross-Sectional Data:** The dataset represents a point-in-time snapshot, not a historical inventory movement ledger with time-stamped stock entries/exits.
- **Illustrative Working Capital:** Balance sheet accounts are corporate finance simulations based on benchmark industry financial statements.

---

## 15. Future Scope

- **Machine Learning Valuation API:** Train gradient boosting models (XGBoost / LightGBM) on the cleaned dataset to predict fair vehicle market value.
- **Real-Time Web Scraper Integration:** Extend the data loader to ingest live listings from CarDekho and CarWale APIs.
- **Direct ERP / DMS Integration:** Connect the working capital calculator to dealership management systems (CDK Global, Reynolds and Reynolds) for real-time general ledger tracking.

---

## 16. Installation & Execution Guide

### Prerequisites
- Python 3.10+ (tested on Python 3.13.1)
- Git

### 1. Clone Repository & Setup Environment
```bash
git clone https://github.com/<your-username>/automotive-dealership-profitability-analysis.git
cd automotive-dealership-profitability-analysis
python -m venv venv
venv\Scripts\activate  # On Windows PowerShell: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Execute Data Pipeline & Analyses
```bash
# 1. Clean raw dataset & generate derived dimensions
python src/data_cleaning.py

# 2. Run exploratory analysis & generate 9 charts
python src/vehicle_analysis.py

# 3. Run unit economics profitability scenario model
python src/profitability_scenario.py

# 4. Run corporate working capital scenario simulation
python src/working_capital.py

# 5. Generate 11-sheet Advanced Excel Workbook
python src/excel_generator.py

# 6. Initialize SQLite DB & execute 20 business queries
python sql/init_database.py
python sql/run_queries.py

# 7. Export Power BI tables
python powerbi/prepare_powerbi_data.py

# 8. Compile Markdown & PDF Executive Management Reports
python src/report_generator.py
```

### 3. Run Automated Tests
```bash
pytest tests/test_analysis.py -v
```

### 4. Launch Interactive Streamlit Portal
```bash
streamlit run dashboard/app.py
```

---

## 17. GitHub Deployment Commands

To push this repository to GitHub:

```bash
# Initialize git if not already initialized
git init

# Add all files
git add .

# Initial commit
git commit -m "feat: complete automotive dealership profitability & working capital analytics solution"

# Add your remote GitHub repository
git remote add origin https://github.com/<your-username>/automotive-dealership-profitability-analysis.git

# Set main branch and push
git branch -M main
git push -u origin main
```

---

## 18. Verification Checklist

- [x] **Real Dataset Ingested:** Sourced from Kaggle (`Car details v3.csv`, 8,128 raw rows).
- [x] **Data Provenance Recorded:** Unchanged raw copies preserved in `data/raw/`.
- [x] **Zero Synthetic Records:** No fake vehicle transactions or artificial accounting ledgers mixed in.
- [x] **Data Cleaning Executed:** 1,202 duplicates removed; 6,926 unique records saved in `data/processed/cleaned_vehicle_data.csv`.
- [x] **Derived Dimensions Engineered:** `Vehicle_Brand`, `Vehicle_Model`, `Vehicle_Age` (2026), `Price_Category`, `Mileage_Category`, `Kilometres_Category`, etc.
- [x] **Exploratory Visualizations Created:** 11 charts generated in `outputs/charts/`.
- [x] **Unit Economics Scenario Model Built:** Configurable assumptions, gross profit, gross margin %, net contribution.
- [x] **Working Capital Model Built:** Current Ratio, Quick Ratio, Inventory Turnover, DSI, DSO, DPO, CCC, carrying drag across 3 benchmark scenarios.
- [x] **Advanced Excel Workbook Built:** 11 sheets in `excel/Automotive_Dealership_Analysis.xlsx` with native formulas and charts.
- [x] **SQLite Database & 20 Queries Implemented:** Schema, data ingested, all 20 business queries executed cleanly.
- [x] **Power BI Deliverables Prepared:** Star schema model, 25+ DAX measures, setup guide, and 5 pre-exported CSV tables.
- [x] **Streamlit Web Application Built:** 7 interactive pages with dynamic filters and download options.
- [x] **Management Report Generated:** 14 structured sections in Markdown and PDF format.
- [x] **Automated Tests Implemented & Passing:** 16 pytest unit tests passing 100%.
- [x] **Clear Governance Disclaimers:** Explicit distinction between observed market listings and hypothetical financial scenarios throughout.

---
*Developed for Institutional Corporate Finance, Automotive Dealership Management, and Investment Analysis.*
