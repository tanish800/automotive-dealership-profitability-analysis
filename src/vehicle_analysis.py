"""
=============================================================================
MODULE: vehicle_analysis.py
PROJECT: Automotive Dealership Profitability & Working Capital Analysis
AUTHOR: Senior Financial Analyst & Automotive Consultant
DATASET: Vehicle Dataset from CarDekho (Kaggle)
=============================================================================

PURPOSE:
Conducts rigorous exploratory data analysis (EDA) and market pricing analysis
on real CarDekho used-car listings. Computes summary metrics, group-wise
aggregations, depreciation curves, and exports professional visualizations.

DISCLAIMER:
All metrics represent listing-level observations (asking prices and marketplace
inventory characteristics), NOT verified dealership sales transactions or
dealer internal accounting records.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure headless matplotlib backend
plt.switch_backend("Agg")

# Directory setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_vehicle_data.csv")
CHARTS_DIR = os.path.join(BASE_DIR, "outputs", "charts")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")

# Set visual styling for institutional finance presentation
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.labelweight": "bold",
    "figure.titlesize": 15,
    "figure.titleweight": "bold",
})


def format_inr(val: float) -> str:
    """Formats float value into Indian Lakhs (L) or Crores (Cr)."""
    if pd.isnull(val):
        return "N/A"
    if abs(val) >= 10000000:
        return f"₹{val / 10000000:.2f} Cr"
    elif abs(val) >= 100000:
        return f"₹{val / 100000:.2f} L"
    else:
        return f"₹{val:,.0f}"


def calculate_market_kpis(df: pd.DataFrame) -> dict:
    """
    Computes core listing-level market observation KPIs.
    """
    kpis = {
        "total_listings": int(len(df)),
        "avg_selling_price": float(df["selling_price"].mean()),
        "median_selling_price": float(df["selling_price"].median()),
        "min_selling_price": float(df["selling_price"].min()),
        "max_selling_price": float(df["selling_price"].max()),
        "std_selling_price": float(df["selling_price"].std()),
        "avg_km_driven": float(df["km_driven"].mean()),
        "median_km_driven": float(df["km_driven"].median()),
        "avg_vehicle_age": float(df["Vehicle_Age"].mean()),
        "median_vehicle_age": float(df["Vehicle_Age"].median()),
        "total_brands": int(df["Vehicle_Brand"].nunique()),
        "total_models": int(df["Vehicle_Model"].nunique()),
        "total_gross_listing_value": float(df["selling_price"].sum()),
    }
    return kpis


def brand_analysis(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Computes brand-wise volume, pricing, and market share statistics."""
    grouped = df.groupby("Vehicle_Brand").agg(
        listing_count=("selling_price", "count"),
        avg_price=("selling_price", "mean"),
        median_price=("selling_price", "median"),
        min_price=("selling_price", "min"),
        max_price=("selling_price", "max"),
        std_price=("selling_price", "std"),
        avg_km=("km_driven", "mean"),
        avg_age=("Vehicle_Age", "mean"),
        total_listing_value=("selling_price", "sum"),
    ).reset_index()

    grouped["market_share_pct"] = (grouped["listing_count"] / len(df)) * 100
    grouped["value_share_pct"] = (grouped["total_listing_value"] / df["selling_price"].sum()) * 100
    grouped = grouped.sort_values(by="listing_count", ascending=False).reset_index(drop=True)
    return grouped


def model_analysis(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Computes model-wise performance metrics for the most liquid models."""
    grouped = df.groupby(["Vehicle_Brand", "Vehicle_Model"]).agg(
        listing_count=("selling_price", "count"),
        avg_price=("selling_price", "mean"),
        median_price=("selling_price", "median"),
        avg_km=("km_driven", "mean"),
        avg_age=("Vehicle_Age", "mean"),
    ).reset_index()

    grouped["market_share_pct"] = (grouped["listing_count"] / len(df)) * 100
    grouped = grouped.sort_values(by="listing_count", ascending=False).head(top_n).reset_index(drop=True)
    return grouped


def fuel_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Computes fuel-wise listing counts, pricing, and fuel economy metrics."""
    grouped = df.groupby("Fuel_Category").agg(
        listing_count=("selling_price", "count"),
        avg_price=("selling_price", "mean"),
        median_price=("selling_price", "median"),
        avg_km=("km_driven", "mean"),
        avg_mileage=("Mileage_kmpl", "mean"),
        avg_age=("Vehicle_Age", "mean"),
    ).reset_index()
    grouped["listing_share_pct"] = (grouped["listing_count"] / len(df)) * 100
    return grouped.sort_values(by="listing_count", ascending=False).reset_index(drop=True)


def transmission_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyzes price premium of Automatic vs Manual transmission listings."""
    grouped = df.groupby("Transmission_Category").agg(
        listing_count=("selling_price", "count"),
        avg_price=("selling_price", "mean"),
        median_price=("selling_price", "median"),
        avg_km=("km_driven", "mean"),
        avg_age=("Vehicle_Age", "mean"),
    ).reset_index()
    grouped["listing_share_pct"] = (grouped["listing_count"] / len(df)) * 100
    return grouped


def ownership_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyzes impact of ownership history on vehicle market valuation."""
    grouped = df.groupby("Ownership_Category").agg(
        listing_count=("selling_price", "count"),
        avg_price=("selling_price", "mean"),
        median_price=("selling_price", "median"),
        avg_km=("km_driven", "mean"),
        avg_age=("Vehicle_Age", "mean"),
    ).reset_index()

    first_owner_avg = grouped.loc[grouped["Ownership_Category"] == "First Owner", "avg_price"]
    base_price = first_owner_avg.values[0] if len(first_owner_avg) > 0 else grouped["avg_price"].max()
    grouped["discount_vs_first_owner_pct"] = ((grouped["avg_price"] - base_price) / base_price) * 100
    grouped["listing_share_pct"] = (grouped["listing_count"] / len(df)) * 100
    return grouped.sort_values(by="avg_price", ascending=False).reset_index(drop=True)


def seller_type_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Compares listings posted by Dealers, Trustmark Dealers, and Individuals."""
    grouped = df.groupby("Seller_Category").agg(
        listing_count=("selling_price", "count"),
        avg_price=("selling_price", "mean"),
        median_price=("selling_price", "median"),
        avg_km=("km_driven", "mean"),
        avg_age=("Vehicle_Age", "mean"),
    ).reset_index()
    grouped["listing_share_pct"] = (grouped["listing_count"] / len(df)) * 100
    return grouped.sort_values(by="listing_count", ascending=False).reset_index(drop=True)


def price_category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Segments marketplace listings across entry-level, mid-tier, and luxury brackets."""
    grouped = df.groupby("Price_Category").agg(
        listing_count=("selling_price", "count"),
        avg_price=("selling_price", "mean"),
        median_price=("selling_price", "median"),
        avg_km=("km_driven", "mean"),
        avg_age=("Vehicle_Age", "mean"),
        total_value=("selling_price", "sum"),
    ).reset_index()
    grouped["volume_share_pct"] = (grouped["listing_count"] / len(df)) * 100
    grouped["value_share_pct"] = (grouped["total_value"] / df["selling_price"].sum()) * 100
    return grouped.sort_values(by="total_value", ascending=False).reset_index(drop=True)


def generate_all_visualizations(df: pd.DataFrame) -> list[str]:
    """Generates and saves all 9 visual analytics figures."""
    os.makedirs(CHARTS_DIR, exist_ok=True)
    generated_charts = []

    # Chart 1: Brand Distribution (Top 10 Volume)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_brands = df["Vehicle_Brand"].value_counts().head(10)
    bars = ax.barh(top_brands.index[::-1], top_brands.values[::-1], color="#1B365D", edgecolor="#0F1E33", alpha=0.85)
    ax.set_title("Market Concentration: Top 10 Automotive Brands by Listing Volume", pad=15)
    ax.set_xlabel("Number of Vehicle Listings")
    for bar in bars:
        w = bar.get_width()
        pct = (w / len(df)) * 100
        ax.text(w + 25, bar.get_y() + bar.get_height() / 2, f"{w:,} ({pct:.1f}%)", va="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    p1 = os.path.join(CHARTS_DIR, "brand_distribution.png")
    fig.savefig(p1, dpi=300)
    plt.close(fig)
    generated_charts.append(p1)

    # Chart 2: Selling Price Distribution (Log / Lakhs)
    fig, ax = plt.subplots(figsize=(10, 6))
    prices_lakhs = df["selling_price"] / 100000
    sns.histplot(prices_lakhs[prices_lakhs <= 25], kde=True, bins=40, color="#2B5B84", ax=ax)
    median_val = prices_lakhs.median()
    mean_val = prices_lakhs.mean()
    ax.axvline(median_val, color="#D9534F", linestyle="--", linewidth=2, label=f"Median: ₹{median_val:.2f}L")
    ax.axvline(mean_val, color="#F0AD4E", linestyle="-.", linewidth=2, label=f"Mean: ₹{mean_val:.2f}L")
    ax.set_title("Distribution of Vehicle Listed Selling Prices (Truncated at ₹25L)", pad=15)
    ax.set_xlabel("Listing Price (₹ Lakhs)")
    ax.set_ylabel("Listing Frequency")
    ax.legend(frameon=True)
    plt.tight_layout()
    p2 = os.path.join(CHARTS_DIR, "selling_price_distribution.png")
    fig.savefig(p2, dpi=300)
    plt.close(fig)
    generated_charts.append(p2)

    # Chart 3: Fuel Type & Transmission Breakdown
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fuel_counts = df["Fuel_Category"].value_counts()
    ax1.pie(fuel_counts.values, labels=fuel_counts.index, autopct="%1.1f%%",
            colors=["#1B365D", "#4B779A", "#88A6BF", "#D3DFEE"], startangle=140,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax1.set_title("Listing Share by Fuel Type")

    trans_counts = df["Transmission_Category"].value_counts()
    ax2.pie(trans_counts.values, labels=trans_counts.index, autopct="%1.1f%%",
            colors=["#2A6F97", "#A9D6E5"], startangle=90,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax2.set_title("Listing Share by Transmission")
    plt.tight_layout()
    p3 = os.path.join(CHARTS_DIR, "fuel_and_transmission_distribution.png")
    fig.savefig(p3, dpi=300)
    plt.close(fig)
    generated_charts.append(p3)

    # Chart 4: Brand Pricing Analysis (Top 12 Brands Mean vs Median)
    fig, ax = plt.subplots(figsize=(11, 6))
    top_brands_list = df["Vehicle_Brand"].value_counts().head(12).index
    brand_sub = df[df["Vehicle_Brand"].isin(top_brands_list)].groupby("Vehicle_Brand")["selling_price"].agg(["mean", "median"]).loc[top_brands_list] / 100000
    x = np.arange(len(top_brands_list))
    width = 0.38
    ax.bar(x - width/2, brand_sub["mean"], width, label="Mean Asking Price", color="#1F4E79")
    ax.bar(x + width/2, brand_sub["median"], width, label="Median Asking Price", color="#5B9BD5")
    ax.set_xticks(x)
    ax.set_xticklabels(top_brands_list, rotation=40, ha="right")
    ax.set_ylabel("Price (₹ Lakhs)")
    ax.set_title("Comparative Brand Pricing: Top 12 Automotive Manufacturers", pad=15)
    ax.legend(frameon=True)
    plt.tight_layout()
    p4 = os.path.join(CHARTS_DIR, "brand_pricing_analysis.png")
    fig.savefig(p4, dpi=300)
    plt.close(fig)
    generated_charts.append(p4)

    # Chart 5: Age Depreciation Curve
    fig, ax = plt.subplots(figsize=(10, 6))
    age_trend = df[df["Vehicle_Age"] <= 20].groupby("Vehicle_Age")["selling_price"].agg(["median", "mean"]) / 100000
    ax.plot(age_trend.index, age_trend["median"], marker="o", color="#1B365D", linewidth=2.5, label="Median Price (₹ Lakhs)")
    ax.plot(age_trend.index, age_trend["mean"], marker="s", linestyle="--", color="#E67E22", linewidth=2, label="Mean Price (₹ Lakhs)")
    ax.set_title("Automotive Depreciation Profile: Selling Price vs. Vehicle Age", pad=15)
    ax.set_xlabel("Vehicle Age (Years from 2026 Baseline)")
    ax.set_ylabel("Asking Price (₹ Lakhs)")
    ax.legend(frameon=True)
    ax.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    p5 = os.path.join(CHARTS_DIR, "age_depreciation_curve.png")
    fig.savefig(p5, dpi=300)
    plt.close(fig)
    generated_charts.append(p5)

    # Chart 6: KM Driven vs Price Scatter
    fig, ax = plt.subplots(figsize=(10, 6))
    sub_scatter = df[(df["km_driven"] <= 200000) & (df["selling_price"] <= 3000000)].sample(min(2000, len(df)), random_state=42)
    sns.scatterplot(x=sub_scatter["km_driven"] / 1000, y=sub_scatter["selling_price"] / 100000,
                    alpha=0.35, color="#2C3E50", ax=ax)
    sns.regplot(x=sub_scatter["km_driven"] / 1000, y=sub_scatter["selling_price"] / 100000,
                scatter=False, ax=ax, color="#E74C3C", line_kws={"linewidth": 2.5})
    ax.set_title("Odometer Utilization vs. Valuation (Sub-₹30L, Sub-200k km)", pad=15)
    ax.set_xlabel("Kilometres Driven ('000 km)")
    ax.set_ylabel("Selling Price (₹ Lakhs)")
    plt.tight_layout()
    p6 = os.path.join(CHARTS_DIR, "km_vs_price_scatter.png")
    fig.savefig(p6, dpi=300)
    plt.close(fig)
    generated_charts.append(p6)

    # Chart 7: Dealer vs Individual Boxplot
    fig, ax = plt.subplots(figsize=(9, 6))
    sub_seller = df[df["selling_price"] <= 2000000].copy()
    sub_seller["price_lakhs"] = sub_seller["selling_price"] / 100000
    sns.boxplot(x="Seller_Category", y="price_lakhs", data=sub_seller, palette=["#34495E", "#2980B9", "#27AE60"], ax=ax)
    ax.set_title("Listing Price Distribution: Dealer vs. Individual Channels (Sub-₹20L)", pad=15)
    ax.set_xlabel("Seller Category")
    ax.set_ylabel("Selling Price (₹ Lakhs)")
    plt.tight_layout()
    p7 = os.path.join(CHARTS_DIR, "dealer_vs_individual_comparison.png")
    fig.savefig(p7, dpi=300)
    plt.close(fig)
    generated_charts.append(p7)

    # Chart 8: Ownership Pricing Impact
    fig, ax = plt.subplots(figsize=(9, 5))
    own_summary = df.groupby("Ownership_Category")["selling_price"].median().sort_values(ascending=False) / 100000
    bars = ax.bar(own_summary.index, own_summary.values, color="#3498DB", edgecolor="#1F4E79", alpha=0.85)
    ax.set_title("Valuation Discount Across Ownership History (Median ₹ Lakhs)", pad=15)
    ax.set_ylabel("Median Price (₹ Lakhs)")
    ax.set_xticklabels(own_summary.index, rotation=20, ha="right")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.1, f"₹{h:.2f}L", ha="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    p8 = os.path.join(CHARTS_DIR, "ownership_pricing_impact.png")
    fig.savefig(p8, dpi=300)
    plt.close(fig)
    generated_charts.append(p8)

    # Chart 9: Price Category Segmentation
    fig, ax = plt.subplots(figsize=(9, 5))
    cat_counts = df["Price_Category"].value_counts()
    order = ["Budget (< ₹3L)", "Mid-Range (₹3L - ₹6L)", "Upper Mid-Range (₹6L - ₹10L)", "Premium (₹10L - ₹20L)", "Luxury (> ₹20L)"]
    cat_counts = cat_counts.reindex(order).dropna()
    bars = ax.bar(cat_counts.index, cat_counts.values, color="#16A085", edgecolor="#0E6655", alpha=0.85)
    ax.set_title("Market Volume Segmentation Across Price Tiers", pad=15)
    ax.set_ylabel("Number of Listings")
    ax.set_xticklabels(cat_counts.index, rotation=25, ha="right")
    for bar in bars:
        h = bar.get_height()
        pct = (h / len(df)) * 100
        ax.text(bar.get_x() + bar.get_width() / 2, h + 25, f"{h:,}\n({pct:.1f}%)", ha="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    p9 = os.path.join(CHARTS_DIR, "price_category_segmentation.png")
    fig.savefig(p9, dpi=300)
    plt.close(fig)
    generated_charts.append(p9)

    print(f"[VEHICLE ANALYSIS] Successfully generated {len(generated_charts)} charts in {CHARTS_DIR}")
    return generated_charts


def run_full_market_analysis() -> dict:
    """Executes all market analytics functions and saves structured summary."""
    df = pd.read_csv(PROCESSED_DATA_PATH)
    kpis = calculate_market_kpis(df)
    brands = brand_analysis(df)
    models = model_analysis(df)
    fuels = fuel_analysis(df)
    transmissions = transmission_analysis(df)
    ownerships = ownership_analysis(df)
    sellers = seller_type_analysis(df)
    price_cats = price_category_analysis(df)
    charts = generate_all_visualizations(df)

    summary_results = {
        "kpis": kpis,
        "top_brands": brands.head(10).to_dict(orient="records"),
        "top_models": models.head(10).to_dict(orient="records"),
        "fuel_breakdown": fuels.to_dict(orient="records"),
        "transmission_breakdown": transmissions.to_dict(orient="records"),
        "ownership_breakdown": ownerships.to_dict(orient="records"),
        "seller_breakdown": sellers.to_dict(orient="records"),
        "price_categories": price_cats.to_dict(orient="records"),
        "charts_generated": charts
    }

    summary_json_path = os.path.join(REPORTS_DIR, "market_analysis_summary.json")
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(summary_results, f, indent=4)

    print(f"[VEHICLE ANALYSIS] Market analysis summary saved to: {summary_json_path}")
    return summary_results


if __name__ == "__main__":
    run_full_market_analysis()
