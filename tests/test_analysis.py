"""
=============================================================================
TEST SUITE: test_analysis.py
PROJECT: Automotive Dealership Profitability & Working Capital Analysis
AUTHOR: Senior Financial Analyst & QA Specialist
=============================================================================

PURPOSE:
Comprehensive automated unit and integration tests using pytest:
- Raw dataset ingestion and provenance
- Data cleaning, deduplication, and derived dimensions
- Vehicle age and pricing category validations
- Profitability scenario unit economics and gross margin calculations
- Working capital formulas, liquidity ratios, and CCC arithmetic
- Edge cases and division-by-zero safeguards
- SQLite database integrity and query execution
- Advanced Excel workbook sheet structure and formula verification
"""

import os
import sys
import sqlite3
import pytest
import pandas as pd
import numpy as np
import openpyxl

# Add src to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from data_loader import load_raw_data, inspect_raw_dataset, get_dataset_metadata
from data_cleaning import parse_brand_and_model, categorize_price, categorize_km, categorize_age, clean_dataset
from profitability_scenario import ProfitabilityScenarioModel
from working_capital import WorkingCapitalModel, compare_scenarios


# -----------------------------------------------------------------------------
# 1. DATA INGESTION & PROVENANCE TESTS
# -----------------------------------------------------------------------------
def test_dataset_provenance_metadata():
    """Verifies dataset provenance and attribution records."""
    meta = get_dataset_metadata()
    assert "CarDekho" in meta["dataset_name"]
    assert "kaggle.com" in meta["source_url"]
    assert meta["primary_file"] == "Car details v3.csv"
    assert "HYPOTHETICAL" in meta["financial_field_notice"] or "SCENARIO" in meta["financial_field_notice"].upper()


def test_raw_data_loader():
    """Tests loading of genuine raw CarDekho CSV."""
    df_raw = load_raw_data()
    assert isinstance(df_raw, pd.DataFrame)
    assert len(df_raw) >= 4340  # Must be at least 4,340 rows (or 8,128 for v3)
    required_cols = ["name", "year", "selling_price", "km_driven", "fuel", "seller_type", "transmission", "owner"]
    for col in required_cols:
        assert col in df_raw.columns, f"Missing required raw column: {col}"


def test_inspect_raw_dataset():
    """Validates summary statistics dictionary from raw dataset."""
    df_raw = load_raw_data()
    info = inspect_raw_dataset(df_raw)
    assert info["record_count"] >= 4340
    assert info["selling_price_min"] > 0
    assert info["selling_price_max"] >= 1000000
    assert info["year_min"] >= 1980
    assert info["year_max"] <= 2026


# -----------------------------------------------------------------------------
# 2. DATA CLEANING & DERIVED DIMENSIONS TESTS
# -----------------------------------------------------------------------------
def test_cleaned_dataset_existence_and_shape():
    """Verifies that cleaned processed data exists with expected schema."""
    cleaned_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_vehicle_data.csv")
    assert os.path.exists(cleaned_path), "Cleaned dataset CSV not found"
    df_clean = pd.read_csv(cleaned_path)
    assert len(df_clean) == 6926, f"Expected 6,926 unique records, got {len(df_clean)}"
    assert df_clean.duplicated().sum() == 0, "Cleaned dataset contains unexpected duplicates"


def test_missing_values_in_core_fields():
    """Verifies 0 null values in core operational and financial columns."""
    cleaned_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_vehicle_data.csv")
    df_clean = pd.read_csv(cleaned_path)
    core_cols = [
        "name", "year", "selling_price", "km_driven", "fuel", "seller_type",
        "transmission", "owner", "Vehicle_Brand", "Vehicle_Model", "Vehicle_Age",
        "Price_Category", "Kilometres_Category", "Vehicle_Age_Group"
    ]
    for col in core_cols:
        assert df_clean[col].isnull().sum() == 0, f"Column {col} has unexpected nulls"


def test_brand_model_parsing():
    """Tests parsing logic on single-word and compound OEM brand names."""
    b1, m1 = parse_brand_and_model("Maruti Swift Dzire VDI")
    assert b1 == "Maruti"
    assert "Swift" in m1

    b2, m2 = parse_brand_and_model("Land Rover Discovery Sport SD4")
    assert b2 == "Land Rover"
    assert "Discovery" in m2

    b3, m3 = parse_brand_and_model("Ashok Leyland Stile LE 8-Str")
    assert b3 == "Ashok Leyland"
    assert "Stile" in m3

    b4, m4 = parse_brand_and_model("Hyundai Grand i10 Sportz")
    assert b4 == "Hyundai"
    assert "Grand" in m4


def test_vehicle_age_calculation():
    """Verifies Vehicle_Age = 2026 - year."""
    cleaned_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_vehicle_data.csv")
    df_clean = pd.read_csv(cleaned_path)
    expected_ages = 2026 - df_clean["year"]
    assert (df_clean["Vehicle_Age"] == expected_ages).all()
    assert df_clean["Vehicle_Age"].min() >= 6  # 2020 latest model in dataset
    assert df_clean["Vehicle_Age"].max() <= 50


def test_categorization_functions():
    """Tests categorization boundaries."""
    # Price
    assert categorize_price(200000) == "Budget (< ₹3L)"
    assert categorize_price(450000) == "Mid-Range (₹3L - ₹6L)"
    assert categorize_price(800000) == "Upper Mid-Range (₹6L - ₹10L)"
    assert categorize_price(1500000) == "Premium (₹10L - ₹20L)"
    assert categorize_price(2500000) == "Luxury (> ₹20L)"

    # KM
    assert categorize_km(25000) == "Low (< 30k km)"
    assert categorize_km(45000) == "Moderate (30k - 60k km)"
    assert categorize_km(85000) == "High (60k - 100k km)"
    assert categorize_km(125000) == "Very High (> 100k km)"

    # Age
    assert categorize_age(6) == "Under 7 Years (Recent)"
    assert categorize_age(9) == "7 to 10 Years (Mid-Age)"
    assert categorize_age(13) == "11 to 15 Years (Mature)"
    assert categorize_age(18) == "Over 15 Years (Aged)"


# -----------------------------------------------------------------------------
# 3. PROFITABILITY SCENARIO SIMULATION TESTS
# -----------------------------------------------------------------------------
def test_profitability_scenario_math():
    """Validates unit economics formulas and margin arithmetic."""
    model = ProfitabilityScenarioModel({
        "acquisition_cost_pct": 0.82,
        "discount_pct": 0.04,
        "reconditioning_cost": 15000.0,
        "transportation_cost": 5000.0,
        "other_selling_costs": 8000.0,
    })

    test_df = pd.DataFrame({
        "name": ["Test Car A", "Test Car B"],
        "selling_price": [500000.0, 1000000.0],
    })

    df_res = model.calculate_vehicle_profitability(test_df)

    # Unit 1: ₹5,00,000 list
    # Expected discount: 4% = 20,000
    # Revenue: 480,000
    # Acquisition COGS: 82% = 410,000
    # Gross Profit: 480,000 - 410,000 = 70,000
    # Gross Margin: 70,000 / 480,000 = 14.5833%
    # Direct costs: 15,000 + 5,000 + 8,000 = 28,000
    # Net Contribution: 70,000 - 28,000 = 42,000
    # Net Margin: 42,000 / 480,000 = 8.75%
    row0 = df_res.iloc[0]
    assert row0["Scenario_Revenue"] == pytest.approx(480000.0, 0.01)
    assert row0["Scenario_Acquisition_Cost"] == pytest.approx(410000.0, 0.01)
    assert row0["Scenario_Gross_Profit"] == pytest.approx(70000.0, 0.01)
    assert row0["Scenario_Gross_Margin_Pct"] == pytest.approx(14.5833, 0.01)
    assert row0["Scenario_Net_Contribution"] == pytest.approx(42000.0, 0.01)
    assert row0["Scenario_Net_Margin_Pct"] == pytest.approx(8.75, 0.01)


def test_profitability_scenario_zero_price_handling():
    """Ensures 0 price vehicle does not cause ZeroDivisionError in margin."""
    model = ProfitabilityScenarioModel()
    zero_df = pd.DataFrame({"name": ["Zero Car"], "selling_price": [0.0]})
    res = model.calculate_vehicle_profitability(zero_df)
    assert res.iloc[0]["Scenario_Gross_Margin_Pct"] == 0.0
    assert res.iloc[0]["Scenario_Net_Margin_Pct"] == 0.0


# -----------------------------------------------------------------------------
# 4. WORKING CAPITAL MODEL & LIQUIDITY RATIO TESTS
# -----------------------------------------------------------------------------
def test_working_capital_base_case_metrics():
    """Tests standard corporate finance working capital formulas."""
    wc = WorkingCapitalModel(
        cash_and_bank=5000000,
        accounts_receivable=10000000,
        inventory_value=27500000,
        other_current_assets=2500000,
        accounts_payable=14000000,
        short_term_borrowings=11000000,
        other_current_liabilities=3000000,
        annual_credit_sales=180000000,
        annual_cogs=150000000,
        annual_credit_purchases=155000000,
    )
    m = wc.compute_all_metrics()

    # Total CA: 50L + 100L + 275L + 25L = 450L (₹4.50 Cr)
    assert m["total_current_assets"] == 45000000.0
    # Total CL: 140L + 110L + 30L = 280L (₹2.80 Cr)
    assert m["total_current_liabilities"] == 28000000.0
    # NWC: 4.50 - 2.80 = ₹1.70 Cr
    assert m["net_working_capital"] == 17000000.0
    # Current Ratio: 450 / 280 = 1.607x
    assert m["current_ratio"] == pytest.approx(1.61, 0.01)
    # Quick Ratio: (450 - 275) / 280 = 175 / 280 = 0.625x
    assert m["quick_ratio"] == pytest.approx(0.625, 0.01)
    # DSI: (275L / 1500L) * 365 = 66.92 days
    assert m["inventory_days_dsi"] == pytest.approx(66.9, 0.1)
    # DSO: (100L / 1800L) * 365 = 20.28 days
    assert m["days_sales_outstanding_dso"] == pytest.approx(20.3, 0.1)
    # DPO: (140L / 1550L) * 365 = 32.97 days
    assert m["days_payable_outstanding_dpo"] == pytest.approx(33.0, 0.1)
    # CCC: 66.92 + 20.28 - 32.97 = 54.23 days
    assert m["cash_conversion_cycle_days"] == pytest.approx(54.2, 0.2)


def test_working_capital_division_by_zero_handling():
    """Verifies that 0 liabilities, 0 sales, or 0 COGS do not raise exceptions."""
    wc_zero = WorkingCapitalModel(
        cash_and_bank=1000000,
        accounts_receivable=0,
        inventory_value=0,
        other_current_assets=0,
        accounts_payable=0,
        short_term_borrowings=0,
        other_current_liabilities=0,  # Zero liabilities
        annual_credit_sales=0,        # Zero sales
        annual_cogs=0,                # Zero COGS
        annual_credit_purchases=0     # Zero purchases
    )
    m = wc_zero.compute_all_metrics()
    assert m["current_ratio"] == "N/A"
    assert m["quick_ratio"] == "N/A"
    assert m["inventory_days_dsi"] == 0.0
    assert m["days_sales_outstanding_dso"] == 0.0
    assert m["days_payable_outstanding_dpo"] == 0.0
    assert m["cash_conversion_cycle_days"] == 0.0


def test_scenario_comparison_table():
    """Tests multi-scenario comparison table generation."""
    comp_df = compare_scenarios()
    assert len(comp_df) == 3
    assert "Base Case (Standard Dealership)" in comp_df["Scenario"].values
    assert "Lean Optimized (Fast Velocity)" in comp_df["Scenario"].values
    assert "Stressed (High Lot Aging)" in comp_df["Scenario"].values
    # Lean case CCC must be lower than Base case CCC
    lean_ccc = comp_df.loc[comp_df["Scenario"] == "Lean Optimized (Fast Velocity)", "Cash Conversion Cycle (Days)"].values[0]
    base_ccc = comp_df.loc[comp_df["Scenario"] == "Base Case (Standard Dealership)", "Cash Conversion Cycle (Days)"].values[0]
    assert lean_ccc < base_ccc


# -----------------------------------------------------------------------------
# 5. SQL DATABASE INTEGRITY TESTS
# -----------------------------------------------------------------------------
def test_sqlite_database_and_records():
    """Verifies SQLite dealership.db exists and contains exactly 6,926 records."""
    db_path = os.path.join(BASE_DIR, "sql", "dealership.db")
    assert os.path.exists(db_path), "dealership.db not found"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vehicles;")
    count = cursor.fetchone()[0]
    assert count == 6926, f"Expected 6,926 records in vehicles table, found {count}"

    # Query 1 test: Average selling price by brand
    cursor.execute("SELECT Vehicle_Brand, COUNT(*), AVG(selling_price) FROM vehicles GROUP BY Vehicle_Brand ORDER BY COUNT(*) DESC LIMIT 1;")
    top_brand, b_count, b_avg = cursor.fetchone()
    assert top_brand == "Maruti"
    assert b_count == 2165
    assert b_avg > 300000
    conn.close()


# -----------------------------------------------------------------------------
# 6. EXCEL WORKBOOK INTEGRITY TESTS
# -----------------------------------------------------------------------------
def test_excel_workbook_sheets_and_formatting():
    """Verifies that Automotive_Dealership_Analysis.xlsx has all 11 required sheets."""
    excel_path = os.path.join(BASE_DIR, "excel", "Automotive_Dealership_Analysis.xlsx")
    assert os.path.exists(excel_path), "Excel workbook not found"
    wb = openpyxl.load_workbook(excel_path, data_only=False)

    expected_sheets = [
        "Executive_Summary",
        "Raw_Data",
        "Cleaned_Data",
        "Vehicle_Analysis",
        "Brand_Analysis",
        "Pricing_Analysis",
        "Fuel_Analysis",
        "Ownership_Analysis",
        "Profitability_Scenario",
        "Working_Capital_Model",
        "Financial_KPI_Dashboard",
    ]
    for s_name in expected_sheets:
        assert s_name in wb.sheetnames, f"Missing required worksheet: {s_name}"

    # Verify formula existence in Profitability_Scenario
    ws_prof = wb["Profitability_Scenario"]
    assert str(ws_prof["E15"].value).startswith("="), "Formula missing in Profitability_Scenario row 15"

    # Verify disclaimer in Working_Capital_Model
    ws_wc = wb["Working_Capital_Model"]
    assert "ILLUSTRATIVE" in str(ws_wc["A4"].value).upper() or "ASSUMPTIONS" in str(ws_wc["A4"].value).upper()


# -----------------------------------------------------------------------------
# 7. DELIVERABLE REPORTS TESTS
# -----------------------------------------------------------------------------
def test_generated_reports_and_charts():
    """Verifies existence and non-zero size of generated outputs."""
    md_report = os.path.join(BASE_DIR, "outputs", "reports", "Management_Financial_Report.md")
    pdf_report = os.path.join(BASE_DIR, "outputs", "reports", "Management_Financial_Report.pdf")
    sql_report = os.path.join(BASE_DIR, "sql", "query_results.md")

    assert os.path.exists(md_report) and os.path.getsize(md_report) > 5000
    assert os.path.exists(pdf_report) and os.path.getsize(pdf_report) > 5000
    assert os.path.exists(sql_report) and os.path.getsize(sql_report) > 5000

    charts_dir = os.path.join(BASE_DIR, "outputs", "charts")
    charts = [f for f in os.listdir(charts_dir) if f.endswith(".png")]
    assert len(charts) >= 9, f"Expected at least 9 generated charts, found {len(charts)}"
