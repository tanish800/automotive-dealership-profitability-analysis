"""
=============================================================================
SCRIPT: prepare_powerbi_data.py
PROJECT: Automotive Dealership Profitability & Working Capital Analysis
=============================================================================

PURPOSE:
Generates clean, dimensionally-modeled CSV tables ready for Power BI import:
1. fact_vehicles.csv
2. fact_profitability_scenario.csv
3. fact_working_capital_scenarios.csv
4. dim_brand.csv
5. dim_price_tier.csv
"""

import os
import sys
import pandas as pd

# Add src to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from profitability_scenario import ProfitabilityScenarioModel
from working_capital import compare_scenarios

DATA_DIR = os.path.join(BASE_DIR, "powerbi", "data")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_vehicle_data.csv")


def export_powerbi_tables():
    os.makedirs(DATA_DIR, exist_ok=True)
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # 1. Fact Vehicles
    fact_vehicles_path = os.path.join(DATA_DIR, "fact_vehicles.csv")
    df.to_csv(fact_vehicles_path, index=False)
    print(f"[POWER BI DATA] Exported fact_vehicles.csv ({len(df):,} rows)")

    # 2. Fact Profitability Scenario
    model = ProfitabilityScenarioModel()
    df_prof = model.calculate_vehicle_profitability(df)
    fact_prof_path = os.path.join(DATA_DIR, "fact_profitability_scenario.csv")
    df_prof.to_csv(fact_prof_path, index=False)
    print(f"[POWER BI DATA] Exported fact_profitability_scenario.csv ({len(df_prof):,} rows)")

    # 3. Fact Working Capital Scenarios
    wc_df = compare_scenarios()
    fact_wc_path = os.path.join(DATA_DIR, "fact_working_capital_scenarios.csv")
    wc_df.to_csv(fact_wc_path, index=False)
    print(f"[POWER BI DATA] Exported fact_working_capital_scenarios.csv ({len(wc_df):,} rows)")

    # 4. Dim Brand
    dim_brand = df.groupby("Vehicle_Brand").agg(
        listing_count=("selling_price", "count"),
        avg_price=("selling_price", "mean"),
        median_price=("selling_price", "median"),
        min_price=("selling_price", "min"),
        max_price=("selling_price", "max"),
        total_market_value=("selling_price", "sum"),
    ).reset_index()
    dim_brand["market_share_pct"] = (dim_brand["listing_count"] / len(df)) * 100.0
    dim_brand_path = os.path.join(DATA_DIR, "dim_brand.csv")
    dim_brand.to_csv(dim_brand_path, index=False)
    print(f"[POWER BI DATA] Exported dim_brand.csv ({len(dim_brand):,} brands)")

    # 5. Dim Price Tier
    dim_price = df.groupby("Price_Category").agg(
        listing_count=("selling_price", "count"),
        avg_price=("selling_price", "mean"),
        total_value=("selling_price", "sum"),
        avg_km=("km_driven", "mean"),
        avg_age=("Vehicle_Age", "mean"),
    ).reset_index()
    dim_price["volume_share_pct"] = (dim_price["listing_count"] / len(df)) * 100.0
    dim_price_path = os.path.join(DATA_DIR, "dim_price_tier.csv")
    dim_price.to_csv(dim_price_path, index=False)
    print(f"[POWER BI DATA] Exported dim_price_tier.csv ({len(dim_price):,} tiers)")


if __name__ == "__main__":
    export_powerbi_tables()
