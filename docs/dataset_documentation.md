# DATASET DOCUMENTATION & PROVENANCE SPECIFICATION

**Project Title:** Automotive Dealership Profitability & Working Capital Analysis  
**Repository Name:** `automotive-dealership-profitability-analysis`  
**Dataset Name:** Vehicle Dataset from CarDekho  
**Curator / Author:** Nehal Birla  
**Hosting Platform:** Kaggle  
**Source URL:** [https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho)  
**License:** CC0: Public Domain / Open Database License  
**Acquisition Method:** Programmatic ingestion via KaggleHub API  
**Acquisition Date:** November 02, 2026  
**Analysis Baseline Year:** 2026  

---

## 1. Dataset Overview

The dataset provides real-world listing information for pre-owned passenger vehicles in India scraped from the CarDekho marketplace platform. The raw package on Kaggle contains several historical iterations of the dataset:
- `Car details v3.csv` (8,128 records, 13 attributes including mileage and technical specifications) — **Primary Analysis Dataset**
- `CAR DETAILS FROM CAR DEKHO.csv` (4,340 records, 8 core attributes) — **Base Fallback Dataset**
- `car data.csv` (301 records) — Small sample
- `car details v4.csv` (2,059 records) — Alternate layout

In this project, an unchanged, pristine copy of all original files is preserved in `data/raw/`. The comprehensive version `Car details v3.csv` was processed through our rigorous 10-step data cleaning pipeline to yield `data/processed/cleaned_vehicle_data.csv` (6,926 unique, deduplicated vehicle records).

---

## 2. Raw Schema vs. Cleaned Schema

| Native Column | Native Data Type | Cleaned Derived Column | Cleaned Data Type | Description & Transformation |
| :--- | :--- | :--- | :--- | :--- |
| `name` | String / Object | `name`, `Vehicle_Brand`, `Vehicle_Model` | String | Parsed OEM manufacturer and model line. Handled compound brands (Land Rover, Ashok Leyland, Mercedes-Benz). |
| `year` | Integer | `year`, `Vehicle_Age`, `Vehicle_Age_Group` | Integer / String | Anchored to November 2026 baseline (`Vehicle_Age = 2026 - year`). Categorized into 4 age cohorts. |
| `selling_price` | Float / Integer | `selling_price`, `Price_Category` | Float / String | Listed asking price in INR. Segmented into 5 market tiers (Budget to Luxury). |
| `km_driven` | Float / Integer | `km_driven`, `Kilometres_Category` | Float / String | Odometer reading. Categorized into Low (<30k), Moderate, High, Very High (>100k). |
| `fuel` | String | `fuel`, `Fuel_Category` | String | Diesel, Petrol, CNG, LPG. Title-cased and standardized. |
| `seller_type` | String | `seller_type`, `Seller_Category` | String | Dealer, Individual, Trustmark Dealer. |
| `transmission` | String | `transmission`, `Transmission_Category` | String | Manual, Automatic. |
| `owner` | String | `owner`, `Ownership_Category` | String | First Owner, Second Owner, Third Owner, Fourth & Above Owner, Test Drive Car. |
| `mileage` | Alphanumeric String | `Mileage_kmpl`, `Mileage_Category` | Float / String | Extracted numeric fuel economy (`23.4 kmpl` -> `23.4`). Categorized into Low, Moderate, High. |
| `engine` | Alphanumeric String | `Engine_cc` | Float | Extracted engine displacement in cubic centimeters (`1248 CC` -> `1248.0`). |
| `max_power` | Alphanumeric String | `Max_Power_bhp` | Float | Extracted brake horsepower rating (`74 bhp` -> `74.0`). |
| `seats` | Float | `Seats` | Float | Seating capacity. |

---

## 3. Data Integrity & Deduplication Audit

- **Raw Record Count:** 8,128 records
- **Duplicate Listings Identified:** 1,202 records (14.8% of raw dataset)
- **Rationale for Deduplication:** Pre-owned vehicle marketplaces frequently contain duplicate re-posts by dealers or private individuals reposting the identical vehicle across multiple weeks. Retaining duplicate listings would artificially inflate transaction counts and bias average pricing.
- **Cleaned Population:** **6,926 unique, verified vehicle listings**
- **Missing Values:** 0 null values across all core operational and financial columns (`name`, `year`, `selling_price`, `km_driven`, `fuel`, `seller_type`, `transmission`, `owner`, `Vehicle_Brand`, `Vehicle_Model`, `Vehicle_Age`).

---

## 4. Mandatory Audit Disclaimer

> **IMPORTANT REGULATORY DISCLOSURE:**  
> The underlying dataset contains **asking prices and advertised marketplace listings**. It does **NOT** contain verified dealership wholesale purchase receipts, dealer historical sales invoices, accounts receivable balances, trade payables, or cash ledgers.  
> Consequently, all gross profit margins, net contribution spreads, and working capital cycles generated in this repository are derived from **explicit corporate finance scenario simulation models** clearly separated from observed marketplace figures.
