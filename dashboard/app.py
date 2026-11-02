"""
=============================================================================
STREAMLIT WEB APPLICATION: app.py
PROJECT: Automotive Dealership Profitability & Working Capital Analysis
AUTHOR: Senior Financial Analyst & Full-Stack Python Developer
=============================================================================

PURPOSE:
Interactive financial intelligence and operational analytics portal for
automotive dealership valuation, market pricing, profitability scenarios,
and corporate working capital management.
"""

import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Path Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_vehicle_data.csv")
EXCEL_PATH = os.path.join(BASE_DIR, "excel", "Automotive_Dealership_Analysis.xlsx")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")
SQL_REPORT_PATH = os.path.join(BASE_DIR, "sql", "query_results.md")

# Page Config
st.set_page_config(
    page_title="AutoFinance Intelligence | Dealership Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #1B365D;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 14px;
        color: #555555;
        margin-bottom: 16px;
    }
    .disclaimer-box {
        background-color: #FDEDEC;
        border-left: 5px solid #C0392B;
        padding: 10px 14px;
        margin-bottom: 18px;
        border-radius: 4px;
        font-size: 12px;
        color: #922B21;
        font-weight: 500;
    }
    .metric-card {
        background-color: #F8F9FA;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    if not os.path.exists(PROCESSED_DATA_PATH):
        st.error(f"Processed dataset not found at {PROCESSED_DATA_PATH}. Run src/data_cleaning.py first.")
        st.stop()
    df = pd.read_csv(PROCESSED_DATA_PATH)
    return df


df_all = load_data()

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & GLOBAL FILTERS
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/000000/car--v1.png", width=64)
st.sidebar.title("AutoFinance Hub")
st.sidebar.caption("Automotive Financial & Working Capital Intelligence")

page = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏢 1. Executive Dashboard",
        "🚗 2. Vehicle Market Analysis",
        "🏷️ 3. Brand & Model Analytics",
        "💰 4. Pricing & Valuation",
        "📈 5. Profitability Scenario Model",
        "💼 6. Working Capital Calculator",
        "📄 7. Reports & Downloads"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters (Marketplace)")

# Filters
available_brands = sorted(df_all["Vehicle_Brand"].dropna().unique().tolist())
selected_brands = st.sidebar.multiselect("Automotive Brand", options=available_brands, default=[])

available_fuels = sorted(df_all["Fuel_Category"].dropna().unique().tolist())
selected_fuels = st.sidebar.multiselect("Fuel Type", options=available_fuels, default=[])

available_trans = sorted(df_all["Transmission_Category"].dropna().unique().tolist())
selected_trans = st.sidebar.multiselect("Transmission", options=available_trans, default=[])

available_sellers = sorted(df_all["Seller_Category"].dropna().unique().tolist())
selected_sellers = st.sidebar.multiselect("Seller Category", options=available_sellers, default=[])

min_age = int(df_all["Vehicle_Age"].min())
max_age = int(df_all["Vehicle_Age"].max())
age_range = st.sidebar.slider("Vehicle Age Range (Years)", min_value=min_age, max_value=max_age, value=(min_age, max_age))

min_price = float(df_all["selling_price"].min()) / 100000.0
max_price = float(df_all["selling_price"].max()) / 100000.0
price_range = st.sidebar.slider("Asking Price (₹ Lakhs)", min_value=float(min_price), max_value=float(max_price), value=(min_price, max_price))

# Apply Filter
df_filtered = df_all.copy()
if selected_brands:
    df_filtered = df_filtered[df_filtered["Vehicle_Brand"].isin(selected_brands)]
if selected_fuels:
    df_filtered = df_filtered[df_filtered["Fuel_Category"].isin(selected_fuels)]
if selected_trans:
    df_filtered = df_filtered[df_filtered["Transmission_Category"].isin(selected_trans)]
if selected_sellers:
    df_filtered = df_filtered[df_filtered["Seller_Category"].isin(selected_sellers)]

df_filtered = df_filtered[
    (df_filtered["Vehicle_Age"] >= age_range[0]) &
    (df_filtered["Vehicle_Age"] <= age_range[1]) &
    (df_filtered["selling_price"] >= price_range[0] * 100000) &
    (df_filtered["selling_price"] <= price_range[1] * 100000)
]

st.sidebar.markdown(f"**Filtered Records:** {len(df_filtered):,} of {len(df_all):,}")


def format_inr(val):
    if pd.isnull(val):
        return "N/A"
    if abs(val) >= 10000000:
        return f"₹{val/10000000:.2f} Cr"
    elif abs(val) >= 100000:
        return f"₹{val/100000:.2f} L"
    else:
        return f"₹{val:,.0f}"


# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE DASHBOARD
# -----------------------------------------------------------------------------
if page == "🏢 1. Executive Dashboard":
    st.markdown('<div class="main-header">Automotive Dealership Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Executive Overview of Real Used Vehicle Listings | 2026 Analysis Baseline</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-box">
        <b>REGULATORY AUDIT NOTICE:</b> Metrics presented on this page are derived from real CarDekho marketplace listing observations.
        They reflect asking prices and advertised inventories, NOT internal audited dealership sales transactions.
    </div>
    """, unsafe_allow_html=True)

    # 5 KPI Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Total Listings", f"{len(df_filtered):,}")
    with k2:
        st.metric("Avg Asking Price", format_inr(df_filtered["selling_price"].mean()))
    with k3:
        st.metric("Median Asking Price", format_inr(df_filtered["selling_price"].median()))
    with k4:
        st.metric("Avg Vehicle Age", f"{df_filtered['Vehicle_Age'].mean():.1f} Yrs")
    with k5:
        st.metric("Avg Odometer", f"{df_filtered['km_driven'].mean():,.0f} km")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Market Concentration: Top 10 Brands by Volume")
        top_b = df_filtered["Vehicle_Brand"].value_counts().head(10).reset_index()
        top_b.columns = ["Brand", "Listings"]
        fig1 = px.bar(top_b, x="Listings", y="Brand", orientation="h",
                      color_discrete_sequence=["#1B365D"], text="Listings")
        fig1.update_layout(yaxis={"autorange": "reversed"}, margin=dict(l=10, r=10, t=30, b=10), height=340)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("Listing Price Distribution (₹ Lakhs)")
        prices_lakhs = df_filtered["selling_price"] / 100000.0
        fig2 = px.histogram(prices_lakhs[prices_lakhs <= 25], nbins=35,
                            color_discrete_sequence=["#2A6F97"],
                            labels={"value": "Price (₹ Lakhs)"})
        fig2.update_layout(showlegend=False, margin=dict(l=10, r=10, t=30, b=10), height=340)
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Market Share by Fuel Type")
        fuel_s = df_filtered["Fuel_Category"].value_counts().reset_index()
        fuel_s.columns = ["Fuel", "Count"]
        fig3 = px.pie(fuel_s, names="Fuel", values="Count", hole=0.45,
                      color_discrete_sequence=["#1B365D", "#4B779A", "#88A6BF", "#D3DFEE"])
        fig3.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=300)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.subheader("Listing Channel: Dealer vs. Individual")
        seller_s = df_filtered["Seller_Category"].value_counts().reset_index()
        seller_s.columns = ["Seller Category", "Count"]
        fig4 = px.bar(seller_s, x="Seller Category", y="Count",
                      color="Seller Category", color_discrete_sequence=["#34495E", "#2980B9", "#27AE60"])
        fig4.update_layout(showlegend=False, margin=dict(l=10, r=10, t=30, b=10), height=300)
        st.plotly_chart(fig4, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 2: VEHICLE MARKET ANALYSIS
# -----------------------------------------------------------------------------
elif page == "🚗 2. Vehicle Market Analysis":
    st.markdown('<div class="main-header">Vehicle Market & Operational Characteristics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Depreciation Dynamics, Odometer Utilization, and Ownership Transitions</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Vehicle Age Depreciation Curve")
        age_summary = df_filtered[df_filtered["Vehicle_Age"] <= 20].groupby("Vehicle_Age")["selling_price"].agg(["mean", "median"]).reset_index()
        age_summary["mean"] = age_summary["mean"] / 100000.0
        age_summary["median"] = age_summary["median"] / 100000.0
        fig_age = go.Figure()
        fig_age.add_trace(go.Scatter(x=age_summary["Vehicle_Age"], y=age_summary["mean"], name="Mean Asking Price (₹ L)", mode="lines+markers", line=dict(color="#1B365D", width=2.5)))
        fig_age.add_trace(go.Scatter(x=age_summary["Vehicle_Age"], y=age_summary["median"], name="Median Asking Price (₹ L)", mode="lines+markers", line=dict(color="#E67E22", width=2, dash="dash")))
        fig_age.update_layout(xaxis_title="Vehicle Age (Years)", yaxis_title="Price (₹ Lakhs)", height=380, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_age, use_container_width=True)

    with c2:
        st.subheader("Kilometres Driven vs. Selling Price")
        sub_sample = df_filtered[(df_filtered["km_driven"] <= 200000) & (df_filtered["selling_price"] <= 3000000)]
        if len(sub_sample) > 1500:
            sub_sample = sub_sample.sample(1500, random_state=42)
        fig_scatter = px.scatter(sub_sample, x="km_driven", y="selling_price",
                                 color="Fuel_Category", trendline="ols",
                                 labels={"km_driven": "KM Driven", "selling_price": "Price (₹)"},
                                 color_discrete_sequence=["#1B365D", "#2980B9", "#27AE60", "#E67E22"],
                                 opacity=0.45)
        fig_scatter.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Valuation Discount Across Ownership Tiers")
    own_df = df_filtered.groupby("Ownership_Category").agg(
        Count=("selling_price", "count"),
        Avg_Price=("selling_price", "mean"),
        Median_Price=("selling_price", "median"),
        Avg_KM=("km_driven", "mean"),
        Avg_Age=("Vehicle_Age", "mean")
    ).reset_index()
    first_avg = own_df.loc[own_df["Ownership_Category"] == "First Owner", "Avg_Price"]
    base_val = first_avg.values[0] if len(first_avg) > 0 else own_df["Avg_Price"].max()
    own_df["Discount vs 1st Owner (%)"] = ((own_df["Avg_Price"] - base_val) / base_val) * 100.0

    c3, c4 = st.columns([1, 1])
    with c3:
        fig_own = px.bar(own_df, x="Ownership_Category", y="Median_Price",
                         text=own_df["Median_Price"].apply(format_inr),
                         color_discrete_sequence=["#2A6F97"])
        fig_own.update_layout(yaxis_title="Median Price (₹)", height=320, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_own, use_container_width=True)

    with c4:
        st.markdown("**Ownership Valuation Metrics Table**")
        display_own = own_df.copy()
        display_own["Avg_Price"] = display_own["Avg_Price"].apply(format_inr)
        display_own["Median_Price"] = display_own["Median_Price"].apply(format_inr)
        display_own["Avg_KM"] = display_own["Avg_KM"].apply(lambda x: f"{x:,.0f} km")
        display_own["Avg_Age"] = display_own["Avg_Age"].apply(lambda x: f"{x:.1f} Yrs")
        display_own["Discount vs 1st Owner (%)"] = display_own["Discount vs 1st Owner (%)"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_own, hide_index=True, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 3: BRAND AND MODEL ANALYSIS
# -----------------------------------------------------------------------------
elif page == "🏷️ 3. Brand & Model Analytics":
    st.markdown('<div class="main-header">Brand & Model Level Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Manufacturer Market Share, Median Valuation, and Model-Level Liquidity</div>', unsafe_allow_html=True)

    st.subheader("Top Automotive Brands: Comparative Volume & Asking Price")
    top_brands = df_filtered["Vehicle_Brand"].value_counts().head(12).index.tolist()
    brand_perf = df_filtered[df_filtered["Vehicle_Brand"].isin(top_brands)].groupby("Vehicle_Brand").agg(
        Listings=("selling_price", "count"),
        Mean_Price=("selling_price", "mean"),
        Median_Price=("selling_price", "median"),
        Total_Value=("selling_price", "sum")
    ).loc[top_brands].reset_index()

    fig_bm = go.Figure()
    fig_bm.add_trace(go.Bar(x=brand_perf["Vehicle_Brand"], y=brand_perf["Mean_Price"] / 100000.0, name="Mean Asking Price (₹ L)", marker_color="#1B365D"))
    fig_bm.add_trace(go.Bar(x=brand_perf["Vehicle_Brand"], y=brand_perf["Median_Price"] / 100000.0, name="Median Asking Price (₹ L)", marker_color="#5B9BD5"))
    fig_bm.update_layout(barmode="group", yaxis_title="Price (₹ Lakhs)", height=380, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_bm, use_container_width=True)

    st.subheader("Top 15 Most Liquid Vehicle Models in Marketplace")
    model_perf = df_filtered.groupby(["Vehicle_Brand", "Vehicle_Model"]).agg(
        Listings=("selling_price", "count"),
        Avg_Price=("selling_price", "mean"),
        Median_Price=("selling_price", "median"),
        Avg_KM=("km_driven", "mean"),
        Avg_Age=("Vehicle_Age", "mean")
    ).reset_index().sort_values(by="Listings", ascending=False).head(15)

    model_perf["Avg_Price"] = model_perf["Avg_Price"].apply(format_inr)
    model_perf["Median_Price"] = model_perf["Median_Price"].apply(format_inr)
    model_perf["Avg_KM"] = model_perf["Avg_KM"].apply(lambda x: f"{x:,.0f} km")
    model_perf["Avg_Age"] = model_perf["Avg_Age"].apply(lambda x: f"{x:.1f} Yrs")
    st.dataframe(model_perf, hide_index=True, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 4: PRICING ANALYSIS
# -----------------------------------------------------------------------------
elif page == "💰 4. Pricing & Valuation":
    st.markdown('<div class="main-header">Marketplace Pricing Segmentation & Valuation Tiers</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Distribution across Budget, Mid-Range, Premium, and Luxury Segments</div>', unsafe_allow_html=True)

    cat_order = ["Budget (< ₹3L)", "Mid-Range (₹3L - ₹6L)", "Upper Mid-Range (₹6L - ₹10L)", "Premium (₹10L - ₹20L)", "Luxury (> ₹20L)"]
    cat_summary = df_filtered.groupby("Price_Category").agg(
        Volume=("selling_price", "count"),
        Total_Value=("selling_price", "sum"),
        Avg_Price=("selling_price", "mean"),
        Avg_KM=("km_driven", "mean"),
        Avg_Age=("Vehicle_Age", "mean")
    ).reindex(cat_order).dropna().reset_index()

    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Inventory Capital Allocation by Price Tier")
        fig_cap = px.pie(cat_summary, names="Price_Category", values="Total_Value", hole=0.45,
                         color_discrete_sequence=["#1B365D", "#2980B9", "#27AE60", "#E67E22", "#C0392B"])
        fig_cap.update_layout(height=340, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_cap, use_container_width=True)

    with c2:
        st.subheader("Listing Count by Price Tier")
        fig_vol = px.bar(cat_summary, x="Price_Category", y="Volume",
                         text="Volume", color_discrete_sequence=["#16A085"])
        fig_vol.update_layout(height=340, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_vol, use_container_width=True)

    st.subheader("Price Tier Breakdown Table")
    disp_cat = cat_summary.copy()
    disp_cat["Total_Value"] = disp_cat["Total_Value"].apply(format_inr)
    disp_cat["Avg_Price"] = disp_cat["Avg_Price"].apply(format_inr)
    disp_cat["Avg_KM"] = disp_cat["Avg_KM"].apply(lambda x: f"{x:,.0f} km")
    disp_cat["Avg_Age"] = disp_cat["Avg_Age"].apply(lambda x: f"{x:.1f} Yrs")
    st.dataframe(disp_cat, hide_index=True, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 5: PROFITABILITY SCENARIO CALCULATOR
# -----------------------------------------------------------------------------
elif page == "📈 5. Profitability Scenario Model":
    st.markdown('<div class="main-header">Dealership Profitability Scenario Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Parametric Unit Economics & Gross Margin Simulation Model</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-box">
        <b>MANDATORY COMPLIANCE NOTICE:</b>
        HYPOTHETICAL FINANCIAL SCENARIO – NOT ACTUAL DEALERSHIP ACCOUNTING DATA.
        CarDekho dataset contains listing asking prices. Wholesale vehicle buy-in costs, discounts,
        and reconditioning expenses are user-configurable assumptions below.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("1. Configure Unit Economics Assumptions")
    a1, a2, a3, a4, a5 = st.columns(5)
    with a1:
        acq_pct = st.slider("Acquisition Cost (% of List)", min_value=70, max_value=90, value=82, step=1) / 100.0
    with a2:
        disc_pct = st.slider("Negotiation Discount (%)", min_value=0, max_value=10, value=4, step=1) / 100.0
    with a3:
        recond_cost = st.number_input("Reconditioning Cost (₹)", min_value=0, max_value=100000, value=15000, step=2500)
    with a4:
        trans_cost = st.number_input("Logistics / Transport (₹)", min_value=0, max_value=50000, value=5000, step=1000)
    with a5:
        other_cost = st.number_input("Other Selling Expenses (₹)", min_value=0, max_value=50000, value=8000, step=1000)

    # Dynamic Simulation on Filtered Listings
    df_sim = df_filtered.copy()
    df_sim["Scenario_Price"] = df_sim["selling_price"]
    df_sim["Scenario_Discount"] = df_sim["Scenario_Price"] * disc_pct
    df_sim["Scenario_Revenue"] = df_sim["Scenario_Price"] - df_sim["Scenario_Discount"]
    df_sim["Scenario_Acq_Cost"] = df_sim["Scenario_Price"] * acq_pct
    df_sim["Scenario_Gross_Profit"] = df_sim["Scenario_Revenue"] - df_sim["Scenario_Acq_Cost"]
    df_sim["Scenario_Direct_Costs"] = recond_cost + trans_cost + other_cost
    df_sim["Scenario_Net_Contribution"] = df_sim["Scenario_Gross_Profit"] - df_sim["Scenario_Direct_Costs"]

    tot_rev = df_sim["Scenario_Revenue"].sum()
    tot_gp = df_sim["Scenario_Gross_Profit"].sum()
    tot_net = df_sim["Scenario_Net_Contribution"].sum()
    gm_pct = (tot_gp / tot_rev * 100.0) if tot_rev > 0 else 0.0
    net_pct = (tot_net / tot_rev * 100.0) if tot_rev > 0 else 0.0

    st.markdown("---")
    st.subheader("2. Portfolio Simulation Scorecard")
    s1, s2, s3, s4, s5 = st.columns(5)
    with s1:
        st.metric("Simulated Revenue", format_inr(tot_rev))
    with s2:
        st.metric("Simulated Gross Profit", format_inr(tot_gp))
    with s3:
        st.metric("Simulated Gross Margin", f"{gm_pct:.1f}%")
    with s4:
        st.metric("Net Contribution", format_inr(tot_net))
    with s5:
        st.metric("Net Margin %", f"{net_pct:.1f}%")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 10 Brands: Scenario Revenue vs Gross Profit")
        brand_sim = df_sim.groupby("Vehicle_Brand").agg(
            Revenue=("Scenario_Revenue", "sum"),
            Gross_Profit=("Scenario_Gross_Profit", "sum"),
            Net_Contrib=("Scenario_Net_Contribution", "sum")
        ).sort_values(by="Revenue", ascending=False).head(10).reset_index()

        fig_bgp = go.Figure()
        fig_bgp.add_trace(go.Bar(x=brand_sim["Vehicle_Brand"], y=brand_sim["Gross_Profit"] / 10000000.0, name="Gross Profit (₹ Cr)", marker_color="#1F4E79"))
        fig_bgp.add_trace(go.Bar(x=brand_sim["Vehicle_Brand"], y=brand_sim["Net_Contrib"] / 10000000.0, name="Net Contribution (₹ Cr)", marker_color="#27AE60"))
        fig_bgp.update_layout(barmode="group", yaxis_title="Profit (₹ Crores)", height=350, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_bgp, use_container_width=True)

    with c2:
        st.subheader("Scenario Net Contribution Margin % by Price Tier")
        cat_sim = df_sim.groupby("Price_Category").agg(
            Revenue=("Scenario_Revenue", "sum"),
            Net_Contrib=("Scenario_Net_Contribution", "sum")
        ).reindex(cat_order).dropna().reset_index()
        cat_sim["Net_Margin_Pct"] = (cat_sim["Net_Contrib"] / cat_sim["Revenue"]) * 100.0

        fig_ncm = px.bar(cat_sim, x="Price_Category", y="Net_Margin_Pct",
                         text=cat_sim["Net_Margin_Pct"].apply(lambda x: f"{x:.1f}%"),
                         color_discrete_sequence=["#E67E22"])
        fig_ncm.update_layout(yaxis_title="Net Margin (%)", height=350, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_ncm, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 6: WORKING CAPITAL CALCULATOR
# -----------------------------------------------------------------------------
elif page == "💼 6. Working Capital Calculator":
    st.markdown('<div class="main-header">Corporate Working Capital & Liquidity Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Cash Conversion Cycle (CCC), Turnover Multiples, and Floor-Plan Carrying Drag</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-box">
        <b>REGULATORY AUDIT NOTICE:</b>
        ILLUSTRATIVE WORKING CAPITAL MODEL – USER-ENTERED ASSUMPTIONS.
        The real CarDekho dataset does not contain balance sheet accounts (AR, AP, Cash, Inventory Values).
        All calculations below are corporate finance simulation formulas based on user parameters.
    </div>
    """, unsafe_allow_html=True)

    # Preset Loader Buttons
    st.subheader("1. Select Industry Benchmark Preset or Customize")
    p1, p2, p3 = st.columns(3)
    preset_choice = "Base Case"
    if p1.button("📋 Load Base Case (Standard Dealership)"):
        st.session_state["wc_ca"] = 4.50
        st.session_state["wc_cl"] = 2.80
        st.session_state["wc_inv"] = 2.75
        st.session_state["wc_sales"] = 18.00
        st.session_state["wc_cogs"] = 15.00
        st.session_state["wc_purch"] = 15.50
        st.session_state["wc_ar"] = 1.00
        st.session_state["wc_ap"] = 1.40
    if p2.button("🚀 Load Lean Optimized (Fast Turn Velocity)"):
        st.session_state["wc_ca"] = 3.20
        st.session_state["wc_cl"] = 2.50
        st.session_state["wc_inv"] = 1.60
        st.session_state["wc_sales"] = 18.00
        st.session_state["wc_cogs"] = 15.00
        st.session_state["wc_purch"] = 15.50
        st.session_state["wc_ar"] = 0.60
        st.session_state["wc_ap"] = 1.80
    if p3.button("⚠️ Load Stressed Case (High Lot Aging)"):
        st.session_state["wc_ca"] = 5.80
        st.session_state["wc_cl"] = 3.40
        st.session_state["wc_inv"] = 3.50
        st.session_state["wc_sales"] = 18.00
        st.session_state["wc_cogs"] = 15.00
        st.session_state["wc_purch"] = 15.50
        st.session_state["wc_ar"] = 1.75
        st.session_state["wc_ap"] = 0.95

    w_ca = st.session_state.get("wc_ca", 4.50)
    w_cl = st.session_state.get("wc_cl", 2.80)
    w_inv = st.session_state.get("wc_inv", 2.75)
    w_sales = st.session_state.get("wc_sales", 18.00)
    w_cogs = st.session_state.get("wc_cogs", 15.00)
    w_purch = st.session_state.get("wc_purch", 15.50)
    w_ar = st.session_state.get("wc_ar", 1.00)
    w_ap = st.session_state.get("wc_ap", 1.40)

    st.markdown("---")
    c_in1, c_in2, c_in3, c_in4 = st.columns(4)
    with c_in1:
        ca_in = st.number_input("Total Current Assets (₹ Cr)", min_value=0.5, max_value=50.0, value=float(w_ca), step=0.25)
        cl_in = st.number_input("Total Current Liabilities (₹ Cr)", min_value=0.5, max_value=50.0, value=float(w_cl), step=0.25)
    with c_in2:
        inv_in = st.number_input("Inventory Carrying Value (₹ Cr)", min_value=0.1, max_value=float(ca_in), value=min(float(w_inv), float(ca_in)), step=0.25)
        ar_in = st.number_input("Accounts Receivable (₹ Cr)", min_value=0.0, max_value=10.0, value=float(w_ar), step=0.10)
    with c_in3:
        sales_in = st.number_input("Annual Credit Sales (₹ Cr)", min_value=1.0, max_value=200.0, value=float(w_sales), step=1.0)
        cogs_in = st.number_input("Annual COGS (₹ Cr)", min_value=1.0, max_value=float(sales_in), value=float(w_cogs), step=1.0)
    with c_in4:
        purch_in = st.number_input("Annual Credit Purchases (₹ Cr)", min_value=1.0, max_value=200.0, value=float(w_purch), step=1.0)
        ap_in = st.number_input("Accounts Payable (₹ Cr)", min_value=0.0, max_value=float(cl_in), value=min(float(w_ap), float(cl_in)), step=0.10)

    # Computations with Safe Division
    nwc = ca_in - cl_in
    current_ratio = ca_in / cl_in if cl_in > 0 else 0.0
    quick_ratio = (ca_in - inv_in) / cl_in if cl_in > 0 else 0.0
    inv_turnover = cogs_in / inv_in if inv_in > 0 else 0.0
    dsi = (inv_in / cogs_in) * 365.0 if cogs_in > 0 else 0.0
    dso = (ar_in / sales_in) * 365.0 if sales_in > 0 else 0.0
    dpo = (ap_in / purch_in) * 365.0 if purch_in > 0 else 0.0
    ccc = dsi + dso - dpo
    carrying_drag = max(0.0, nwc) * 0.105 * 100.0 # in Lakhs at 10.5% debt cost

    st.markdown("---")
    st.subheader("2. Working Capital & Liquidity Output")
    o1, o2, o3, o4, o5 = st.columns(5)
    with o1:
        st.metric("Net Working Capital", f"₹{nwc:.2f} Cr")
    with o2:
        st.metric("Current Ratio", f"{current_ratio:.2f}x")
    with o3:
        st.metric("Quick Ratio", f"{quick_ratio:.2f}x")
    with o4:
        st.metric("Inventory Days (DSI)", f"{dsi:.1f} d")
    with o5:
        st.metric("Cash Conversion Cycle", f"{ccc:.1f} d")

    st.markdown("---")
    c_chart, c_table = st.columns([1, 1])
    with c_chart:
        st.subheader("Operating Cycle Waterfall Components")
        fig_ccc = go.Figure()
        fig_ccc.add_trace(go.Bar(name="Inventory Days (+)", x=["Cycle Days"], y=[dsi], marker_color="#2C3E50"))
        fig_ccc.add_trace(go.Bar(name="Debtor Days (+)", x=["Cycle Days"], y=[dso], marker_color="#2980B9"))
        fig_ccc.add_trace(go.Bar(name="Creditor Days (-)", x=["Cycle Days"], y=[-dpo], marker_color="#E74C3C"))
        fig_ccc.update_layout(barmode="relative", yaxis_title="Days", height=340, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_ccc, use_container_width=True)

    with c_table:
        st.subheader("Liquidity Multiples & Carrying Drag")
        summary_wc = pd.DataFrame([
            {"Metric": "Net Working Capital (₹ Cr)", "Calculated Value": f"₹{nwc:.2f} Cr", "Benchmark Standard": "Positive (> ₹0)"},
            {"Metric": "Current Ratio", "Calculated Value": f"{current_ratio:.2f}x", "Benchmark Standard": "1.30x - 1.50x"},
            {"Metric": "Quick Ratio (Acid-Test)", "Calculated Value": f"{quick_ratio:.2f}x", "Benchmark Standard": ">= 1.00x"},
            {"Metric": "Inventory Turnover", "Calculated Value": f"{inv_turnover:.2f}x", "Benchmark Standard": "6.0x - 9.0x"},
            {"Metric": "Cash Conversion Cycle (CCC)", "Calculated Value": f"{ccc:.1f} days", "Benchmark Standard": "< 45 days"},
            {"Metric": "Annual Floor-Plan Drag @ 10.5%", "Calculated Value": f"₹{carrying_drag:.1f} Lakhs", "Benchmark Standard": "Minimize idle drag"},
        ])
        st.dataframe(summary_wc, hide_index=True, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 7: REPORTS AND DOWNLOADS
# -----------------------------------------------------------------------------
elif page == "📄 7. Reports & Downloads":
    st.markdown('<div class="main-header">Financial Reports, SQL Analytics & Data Export</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Institutional Deliverables, Audit Documentation, and Exportable Files</div>', unsafe_allow_html=True)

    st.subheader("1. Download Deliverables")
    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown("**Cleaned Vehicle Dataset**")
        st.caption("Deduplicated 6,926 records with derived financial dimensions.")
        if os.path.exists(PROCESSED_DATA_PATH):
            with open(PROCESSED_DATA_PATH, "rb") as f:
                st.download_button("📥 Download Cleaned CSV", data=f, file_name="cleaned_vehicle_data.csv", mime="text/csv")

    with d2:
        st.markdown("**Advanced Excel Financial Model**")
        st.caption("11 institutional worksheets with native formulas and charts.")
        if os.path.exists(EXCEL_PATH):
            with open(EXCEL_PATH, "rb") as f:
                st.download_button("📊 Download Excel Workbook", data=f, file_name="Automotive_Dealership_Analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with d3:
        st.markdown("**SQL Business Queries Report**")
        st.caption("Results from all 20 business queries executed on dealership.db.")
        if os.path.exists(SQL_REPORT_PATH):
            with open(SQL_REPORT_PATH, "rb") as f:
                st.download_button("📑 Download SQL Report (MD)", data=f, file_name="sql_query_results.md", mime="text/markdown")

    st.markdown("---")
    st.subheader("2. View In-App Data Audit Documentation")

    doc_tab1, doc_tab2 = st.tabs(["Data Quality Audit Report", "SQL 20 Business Queries Preview"])

    with doc_tab1:
        dq_path = os.path.join(REPORTS_DIR, "data_quality_report.md")
        if os.path.exists(dq_path):
            with open(dq_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info("Data quality report file not found.")

    with doc_tab2:
        if os.path.exists(SQL_REPORT_PATH):
            with open(SQL_REPORT_PATH, "r", encoding="utf-8") as f:
                st.markdown(f.read()[:5000] + "\n\n*(Full report available via download button above)*")
        else:
            st.info("SQL query report file not found.")
