"""
=============================================================================
MODULE: data_loader.py
PROJECT: Automotive Dealership Profitability & Working Capital Analysis
AUTHOR: Senior Financial Analyst & Automotive Consultant
DATASET: Vehicle Dataset from CarDekho (Kaggle)
=============================================================================

PURPOSE:
Loads and inspects the genuine public CarDekho vehicle listing dataset.
Maintains strict data provenance, records metadata, tracks data types,
and ensures that original raw data is never silently modified or replaced.
"""

import os
import json
from datetime import datetime
import pandas as pd


# Default paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PRIMARY_DATASET_FILE = "Car details v3.csv"
FALLBACK_DATASET_FILE = "CAR DETAILS FROM CAR DEKHO.csv"

# Dataset provenance metadata
DATASET_METADATA = {
    "dataset_name": "Vehicle Dataset from CarDekho",
    "source_url": "https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho",
    "author_curator": "Nehal Birla",
    "platform": "Kaggle",
    "license": "CC0: Public Domain / Open Database License",
    "acquisition_method": "KaggleHub direct download",
    "acquisition_date": "2026-11-02",
    "primary_file": PRIMARY_DATASET_FILE,
    "fallback_file": FALLBACK_DATASET_FILE,
    "description": (
        "Real-world automotive used-car listing data scraped from CarDekho. "
        "Contains vehicle listing characteristics including brand/model name, "
        "manufacturing year, listed selling price (INR), kilometres driven, "
        "fuel type, seller type, transmission, ownership count, and technical specifications."
    ),
    "financial_field_notice": (
        "IMPORTANT: The dataset contains listing selling prices (asking prices). "
        "It does NOT contain dealership acquisition invoices, actual historical dealer sales "
        "transactions, dealer COGS, accounts receivable, or accounts payable. "
        "All profitability and working capital calculations must be structured as scenario models."
    )
}


def get_dataset_metadata() -> dict:
    """Returns dataset provenance and attribution metadata."""
    return DATASET_METADATA.copy()


def load_raw_data(filename: str = None) -> pd.DataFrame:
    """
    Loads the genuine CarDekho vehicle dataset from data/raw/.
    Prefers 'Car details v3.csv' (8,128 rows, includes mileage/specs)
    and falls back to 'CAR DETAILS FROM CAR DEKHO.csv' (4,340 rows).

    Parameters:
        filename: Optional specific filename inside data/raw/

    Returns:
        pd.DataFrame containing unchanged raw dataset.
    """
    if filename:
        file_path = os.path.join(RAW_DATA_DIR, filename)
    else:
        primary_path = os.path.join(RAW_DATA_DIR, PRIMARY_DATASET_FILE)
        fallback_path = os.path.join(RAW_DATA_DIR, FALLBACK_DATASET_FILE)

        if os.path.exists(primary_path):
            file_path = primary_path
        elif os.path.exists(fallback_path):
            file_path = fallback_path
        else:
            raise FileNotFoundError(
                f"No genuine CarDekho dataset found in {RAW_DATA_DIR}. "
                f"Please ensure {PRIMARY_DATASET_FILE} or {FALLBACK_DATASET_FILE} is present."
            )

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Specified dataset file not found: {file_path}")

    # Load dataset with strict verification
    df_raw = pd.read_csv(file_path)

    # Validate essential automotive columns
    required_core_cols = ["name", "year", "selling_price", "km_driven", "fuel", "seller_type", "transmission", "owner"]
    missing = [c for c in required_core_cols if c not in df_raw.columns]
    if missing:
        raise ValueError(f"Dataset at {file_path} is missing expected core columns: {missing}")

    return df_raw


def inspect_raw_dataset(df: pd.DataFrame) -> dict:
    """
    Performs initial programmatic inspection of the raw dataset schema,
    memory usage, missing values, duplicates, and statistical bounds.
    """
    inspection = {
        "record_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_counts": {col: int(count) for col, count in df.isnull().sum().items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "year_min": int(df["year"].min()),
        "year_max": int(df["year"].max()),
        "selling_price_min": float(df["selling_price"].min()),
        "selling_price_max": float(df["selling_price"].max()),
        "selling_price_mean": float(df["selling_price"].mean()),
        "selling_price_median": float(df["selling_price"].median()),
        "km_driven_min": float(df["km_driven"].min()),
        "km_driven_max": float(df["km_driven"].max()),
        "km_driven_mean": float(df["km_driven"].mean()),
        "unique_fuels": sorted(df["fuel"].dropna().unique().tolist()),
        "unique_seller_types": sorted(df["seller_type"].dropna().unique().tolist()),
        "unique_transmissions": sorted(df["transmission"].dropna().unique().tolist()),
        "unique_owners": sorted(df["owner"].dropna().unique().tolist()),
    }
    return inspection


if __name__ == "__main__":
    print("=" * 60)
    print("CARDEKHO REAL DATASET LOADER & INSPECTION")
    print("=" * 60)
    df = load_raw_data()
    info = inspect_raw_dataset(df)
    print(f"Loaded records: {info['record_count']:,}")
    print(f"Columns: {info['columns']}")
    print(f"Duplicate rows: {info['duplicate_rows']:,}")
    print(f"Selling price range: INR {info['selling_price_min']:,.0f} - {info['selling_price_max']:,.0f}")
    print(f"Average selling price: INR {info['selling_price_mean']:,.0f}")
    print(f"Median selling price: INR {info['selling_price_median']:,.0f}")
    print(f"Manufacturing year range: {info['year_min']} - {info['year_max']}")
    print("=" * 60)
