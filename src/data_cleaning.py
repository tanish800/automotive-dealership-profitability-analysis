"""
=============================================================================
MODULE: data_cleaning.py
PROJECT: Automotive Dealership Profitability & Working Capital Analysis
AUTHOR: Senior Financial Analyst & Data Analyst
DATASET: Vehicle Dataset from CarDekho (Kaggle)
=============================================================================

PURPOSE:
Cleans, standardizes, validates, and engineers domain-specific financial and
operational features from the genuine CarDekho vehicle listing dataset.
Outputs data/processed/cleaned_vehicle_data.csv and comprehensive data quality reports.
"""

import os
import re
import json
from datetime import datetime
import pandas as pd
import numpy as np

# Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "Car details v3.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_vehicle_data.csv")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")

# Documented Analysis Parameters
ANALYSIS_YEAR = 2026  # Analysis baseline year per current date (November 2026)
TRIM_CODES = {
    "vdi", "vxi", "lxi", "zdi", "zxi", "di", "crdi", "tdi", "exi",
    "gxi", "bsiv", "bsiii", "bsvi", "at", "mt", "amt", "cng", "diesel",
    "petrol", "opt", "plus", "sportz", "magna", "era", "asta"
}


def parse_brand_and_model(vehicle_name: str) -> tuple[str, str]:
    """
    Carefully parses the vehicle listing title to extract brand and model.

    Special Multi-word Brand Handling:
    - 'Land Rover' (parsed from 'Land' or 'Land Rover')
    - 'Ashok Leyland' (parsed from 'Ashok' or 'Ashok Leyland')
    - 'Mercedes-Benz'

    Model Extraction:
    - Extracts 1-2 words following brand.
    - Strips engine, trim codes (VDI, VXI, BSIV) and manufacturing year numbers.
    """
    if not isinstance(vehicle_name, str) or not vehicle_name.strip():
        return "Unknown", "Unknown"

    tokens = vehicle_name.strip().split()
    if not tokens:
        return "Unknown", "Unknown"

    # Multi-word brand parsing
    if len(tokens) >= 2 and tokens[0].lower() == "land" and tokens[1].lower() == "rover":
        brand = "Land Rover"
        rest = tokens[2:]
    elif len(tokens) >= 2 and tokens[0].lower() == "ashok" and tokens[1].lower() == "leyland":
        brand = "Ashok Leyland"
        rest = tokens[2:]
    elif tokens[0].lower() == "ashok":
        brand = "Ashok Leyland"
        rest = tokens[1:]
    elif tokens[0].lower() == "land":
        brand = "Land Rover"
        rest = tokens[1:]
    elif tokens[0].lower() == "mercedes-benz":
        brand = "Mercedes-Benz"
        rest = tokens[1:]
    else:
        brand = tokens[0].capitalize()
        rest = tokens[1:]

    # Model extraction
    model_words = []
    for word in rest:
        clean_word = re.sub(r"[^a-zA-Z0-9]", "", word).lower()
        if clean_word in TRIM_CODES or re.match(r"^(19|20)\d{2}$", clean_word):
            break
        model_words.append(word)
        if len(model_words) >= 2:
            break

    model = " ".join(model_words) if model_words else (rest[0] if rest else "Standard")
    return brand, model


def extract_numeric(val: any) -> float:
    """Extracts first floating-point number from string or returns float value."""
    if pd.isnull(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    match = re.search(r"(\d+\.?\d*)", str(val))
    return float(match.group(1)) if match else np.nan


def categorize_price(price: float) -> str:
    """Categorizes selling price into dealership market tiers in INR."""
    if pd.isnull(price):
        return "Unknown"
    if price < 300000:
        return "Budget (< ₹3L)"
    elif price < 600000:
        return "Mid-Range (₹3L - ₹6L)"
    elif price < 1000000:
        return "Upper Mid-Range (₹6L - ₹10L)"
    elif price < 2000000:
        return "Premium (₹10L - ₹20L)"
    else:
        return "Luxury (> ₹20L)"


def categorize_km(km: float) -> str:
    """Categorizes vehicle odometer reading into usage tiers."""
    if pd.isnull(km):
        return "Unknown"
    if km < 30000:
        return "Low (< 30k km)"
    elif km < 60000:
        return "Moderate (30k - 60k km)"
    elif km < 100000:
        return "High (60k - 100k km)"
    else:
        return "Very High (> 100k km)"


def categorize_age(age: int) -> str:
    """Categorizes vehicle age relative to 2026 analysis baseline."""
    if pd.isnull(age):
        return "Unknown"
    if age <= 7:
        return "Under 7 Years (Recent)"
    elif age <= 10:
        return "7 to 10 Years (Mid-Age)"
    elif age <= 15:
        return "11 to 15 Years (Mature)"
    else:
        return "Over 15 Years (Aged)"


def categorize_mileage(mileage: float) -> str:
    """Categorizes fuel efficiency in kmpl."""
    if pd.isnull(mileage):
        return "Not Specified"
    if mileage < 15.0:
        return "Low (< 15 kmpl)"
    elif mileage <= 20.0:
        return "Moderate (15 - 20 kmpl)"
    else:
        return "High (> 20 kmpl)"


def detect_outliers_iqr(series: pd.Series) -> tuple[float, float, int]:
    """Computes IQR-based lower/upper bounds and outlier count."""
    clean_series = series.dropna()
    q25 = clean_series.quantile(0.25)
    q75 = clean_series.quantile(0.75)
    iqr = q75 - q25
    lower = q25 - 1.5 * iqr
    upper = q75 + 1.5 * iqr
    outliers = clean_series[(clean_series < lower) | (clean_series > upper)].count()
    return lower, upper, int(outliers)


def clean_dataset(input_path: str = None, output_path: str = None, analysis_year: int = ANALYSIS_YEAR) -> pd.DataFrame:
    """
    Executes full data cleaning and feature engineering pipeline on genuine CarDekho data.
    """
    raw_path = input_path or RAW_DATA_PATH
    save_path = output_path or PROCESSED_DATA_PATH

    print(f"[DATA CLEANING] Loading raw dataset from: {raw_path}")
    df_raw = pd.read_csv(raw_path)
    initial_shape = df_raw.shape

    # 1. Missing Value Analysis
    missing_report = df_raw.isnull().sum().to_dict()

    # 2. Duplicate Detection & Deduplication
    initial_duplicates = int(df_raw.duplicated().sum())
    print(f"[DATA CLEANING] Initial records: {initial_shape[0]:,}, Duplicates detected: {initial_duplicates:,}")

    df_clean = df_raw.drop_duplicates().reset_index(drop=True)
    post_dedup_shape = df_clean.shape

    # 3. Categorical Standardization
    df_clean["fuel"] = df_clean["fuel"].astype(str).str.strip().str.title()
    df_clean["seller_type"] = df_clean["seller_type"].astype(str).str.strip().str.title()
    df_clean["transmission"] = df_clean["transmission"].astype(str).str.strip().str.title()
    df_clean["owner"] = df_clean["owner"].astype(str).str.strip().str.title()

    # 4. Brand and Model Extraction
    brand_model_pairs = df_clean["name"].apply(parse_brand_and_model)
    df_clean["Vehicle_Brand"] = [b for b, m in brand_model_pairs]
    df_clean["Vehicle_Model"] = [m for b, m in brand_model_pairs]

    # 5. Technical Specifications Cleaning
    if "mileage" in df_clean.columns:
        df_clean["Mileage_kmpl"] = df_clean["mileage"].apply(extract_numeric)
    else:
        df_clean["Mileage_kmpl"] = np.nan

    if "engine" in df_clean.columns:
        df_clean["Engine_cc"] = df_clean["engine"].apply(extract_numeric)
    else:
        df_clean["Engine_cc"] = np.nan

    if "max_power" in df_clean.columns:
        df_clean["Max_Power_bhp"] = df_clean["max_power"].apply(extract_numeric)
    else:
        df_clean["Max_Power_bhp"] = np.nan

    if "seats" in df_clean.columns:
        df_clean["Seats"] = pd.to_numeric(df_clean["seats"], errors="coerce")
    else:
        df_clean["Seats"] = np.nan

    # 6. Age and Temporal Calculations
    valid_years = (df_clean["year"] >= 1950) & (df_clean["year"] <= analysis_year)
    if not valid_years.all():
        df_clean = df_clean[valid_years].reset_index(drop=True)

    df_clean["Vehicle_Age"] = analysis_year - df_clean["year"]
    df_clean["Vehicle_Age_Group"] = df_clean["Vehicle_Age"].apply(categorize_age)

    # 7. Domain Categorizations
    df_clean["Price_Category"] = df_clean["selling_price"].apply(categorize_price)
    df_clean["Kilometres_Category"] = df_clean["km_driven"].apply(categorize_km)
    df_clean["Mileage_Category"] = df_clean["Mileage_kmpl"].apply(categorize_mileage)
    df_clean["Ownership_Category"] = df_clean["owner"]
    df_clean["Fuel_Category"] = df_clean["fuel"]
    df_clean["Transmission_Category"] = df_clean["transmission"]
    df_clean["Seller_Category"] = df_clean["seller_type"]

    # 8. Outlier Analysis & Tagging
    price_low, price_high, price_outliers = detect_outliers_iqr(df_clean["selling_price"])
    km_low, km_high, km_outliers = detect_outliers_iqr(df_clean["km_driven"])
    age_low, age_high, age_outliers = detect_outliers_iqr(df_clean["Vehicle_Age"])

    df_clean["Is_Price_Outlier"] = (df_clean["selling_price"] < price_low) | (df_clean["selling_price"] > price_high)
    df_clean["Is_KM_Outlier"] = (df_clean["km_driven"] < km_low) | (df_clean["km_driven"] > km_high)

    # 9. Save Processed Dataset
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df_clean.to_csv(save_path, index=False)
    print(f"[DATA CLEANING] Processed dataset saved to: {save_path} ({df_clean.shape[0]:,} rows, {df_clean.shape[1]} cols)")

    # 10. Generate Quality Report
    quality_report = {
        "report_generated_at": datetime.now().isoformat(),
        "analysis_year_baseline": analysis_year,
        "raw_record_count": initial_shape[0],
        "raw_column_count": initial_shape[1],
        "cleaned_record_count": df_clean.shape[0],
        "cleaned_column_count": df_clean.shape[1],
        "duplicate_records_removed": initial_duplicates,
        "missing_values_raw": missing_report,
        "missing_values_cleaned": df_clean.isnull().sum().to_dict(),
        "brand_count": int(df_clean["Vehicle_Brand"].nunique()),
        "model_count": int(df_clean["Vehicle_Model"].nunique()),
    }

    os.makedirs(REPORTS_DIR, exist_ok=True)
    json_report_path = os.path.join(REPORTS_DIR, "data_quality_report.json")
    with open(json_report_path, "w", encoding="utf-8") as f:
        json.dump(quality_report, f, indent=4)

    return df_clean


if __name__ == "__main__":
    clean_dataset()
