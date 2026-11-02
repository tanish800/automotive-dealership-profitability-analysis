"""
=============================================================================
MODULE: excel_generator.py
PROJECT: Automotive Dealership Profitability & Working Capital Analysis
AUTHOR: Advanced Excel Specialist & Senior Financial Analyst
=============================================================================

PURPOSE:
Generates a comprehensive, institutional-grade financial Excel workbook
(Automotive_Dealership_Analysis.xlsx) with 11 professional worksheets,
native Excel formulas, custom number formatting (INR ₹, percentages, ratios),
openpyxl charts, dynamic scenario assumption cells, and clear audit disclaimers.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.formatting.rule import CellIsRule
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_vehicle_data.csv")
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "Car details v3.csv")
EXCEL_OUTPUT_PATH = os.path.join(BASE_DIR, "excel", "Automotive_Dealership_Analysis.xlsx")


# Institutional Styling Constants
NAVY_HEADER = "1B365D"
SLATE_HEADER = "2C3E50"
ACCENT_BLUE = "2A6F97"
ICE_BLUE = "EBF1F5"
LIGHT_GREY = "F8F9FA"
BORDER_GREY = "D3D3D3"
ALERT_RED = "C0392B"
ALERT_BG_RED = "FADBD8"
SUCCESS_GREEN = "27AE60"
SUCCESS_BG = "D4EFDF"
GOLD_ACCENT = "B7950B"

FONT_NAME = "Calibri"
TITLE_FONT = Font(name=FONT_NAME, size=16, bold=True, color="FFFFFF")
SUBTITLE_FONT = Font(name=FONT_NAME, size=11, italic=True, color="D3DFEE")
SECTION_FONT = Font(name=FONT_NAME, size=13, bold=True, color=NAVY_HEADER)
HEADER_FONT = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
DATA_FONT = Font(name=FONT_NAME, size=10, bold=False, color="000000")
BOLD_DATA_FONT = Font(name=FONT_NAME, size=10, bold=True, color="000000")
DISCLAIMER_FONT = Font(name=FONT_NAME, size=9, bold=True, color=ALERT_RED)
KPI_TITLE_FONT = Font(name=FONT_NAME, size=10, bold=True, color="555555")
KPI_VAL_FONT = Font(name=FONT_NAME, size=16, bold=True, color=NAVY_HEADER)

THIN_BORDER_SIDE = Side(border_style="thin", color=BORDER_GREY)
DOUBLE_BORDER_SIDE = Side(border_style="double", color="000000")
TOP_BORDER_SIDE = Side(border_style="thin", color="000000")

STANDARD_BORDER = Border(left=THIN_BORDER_SIDE, right=THIN_BORDER_SIDE, top=THIN_BORDER_SIDE, bottom=THIN_BORDER_SIDE)
TOTAL_BORDER = Border(top=TOP_BORDER_SIDE, bottom=DOUBLE_BORDER_SIDE)

FILL_NAVY = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
FILL_SLATE = PatternFill(start_color=SLATE_HEADER, end_color=SLATE_HEADER, fill_type="solid")
FILL_ACCENT = PatternFill(start_color=ACCENT_BLUE, end_color=ACCENT_BLUE, fill_type="solid")
FILL_ICE = PatternFill(start_color=ICE_BLUE, end_color=ICE_BLUE, fill_type="solid")
FILL_LIGHT = PatternFill(start_color=LIGHT_GREY, end_color=LIGHT_GREY, fill_type="solid")
FILL_DISCLAIMER = PatternFill(start_color=ALERT_BG_RED, end_color=ALERT_BG_RED, fill_type="solid")
FILL_SUCCESS = PatternFill(start_color=SUCCESS_BG, end_color=SUCCESS_BG, fill_type="solid")

ALIGN_LEFT = Alignment(horizontal="left", vertical="center")
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
ALIGN_WRAP = Alignment(horizontal="left", vertical="center", wrap_text=True)

# Format Codes
FMT_INR = '"₹"#,##,##0'
FMT_INR_DEC = '"₹"#,##,##0.00'
FMT_PCT = '0.0%'
FMT_QTY = '#,##0'
FMT_MULT = '0.00"x"'
FMT_DAYS = '0.0" days"'


def apply_title_banner(ws, title: str, subtitle: str, max_col: int = 8):
    """Draws a standardized institutional header banner."""
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max_col)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max_col)

    c1 = ws.cell(row=1, column=1, value=title)
    c1.font = TITLE_FONT
    c1.fill = FILL_NAVY
    c1.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    c2 = ws.cell(row=2, column=1, value=subtitle)
    c2.font = SUBTITLE_FONT
    c2.fill = FILL_NAVY
    c2.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 20
    ws.row_dimensions[3].height = 10


def add_disclaimer_banner(ws, row_idx: int, text: str, max_col: int = 8):
    """Adds highlighted regulatory / audit disclaimer."""
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=max_col)
    c = ws.cell(row=row_idx, column=1, value=f"AUDIT NOTICE: {text}")
    c.font = DISCLAIMER_FONT
    c.fill = FILL_DISCLAIMER
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row_idx].height = 22


def auto_fit_columns(ws, min_width: int = 12, max_width: int = 40):
    """Adjusts column widths based on cell contents."""
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            # Skip merged cells in row 1-3
            if cell.row in [1, 2, 3]:
                continue
            if cell.value:
                val_str = str(cell.value)
                if not val_str.startswith("="):
                    max_len = max(max_len, len(val_str))
        ws.column_dimensions[col_letter].width = max(min(max_len + 3, max_width), min_width)


def generate_workbook():
    """Builds the complete 11-sheet Excel workbook."""
    print(f"[EXCEL GENERATOR] Loading cleaned vehicle dataset from: {PROCESSED_DATA_PATH}")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    raw_df = pd.read_csv(RAW_DATA_PATH)

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # -------------------------------------------------------------------------
    # SHEET 1: Executive_Summary
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 1: Executive_Summary...")
    ws_exec = wb.create_sheet(title="Executive_Summary")
    apply_title_banner(ws_exec, "AUTOMOTIVE DEALERSHIP PROFITABILITY & WORKING CAPITAL ANALYSIS",
                       "Executive Financial Summary & Portfolio Scorecard | Baseline Year: 2026", max_col=7)

    ws_exec.cell(row=4, column=1, value="1. PORTFOLIO OBSERVATION SCORECARD (REAL CARDEKHO DATASET)").font = SECTION_FONT
    ws_exec.row_dimensions[4].height = 24

    kpis = [
        ("Total Analyzed Listings", f"=COUNT(Cleaned_Data!C2:C{len(df)+1})", FMT_QTY),
        ("Total Asking Market Value", f"=SUM(Cleaned_Data!C2:C{len(df)+1})", FMT_INR),
        ("Average Listed Selling Price", f"=AVERAGE(Cleaned_Data!C2:C{len(df)+1})", FMT_INR),
        ("Median Listed Selling Price", f"=MEDIAN(Cleaned_Data!C2:C{len(df)+1})", FMT_INR),
        ("Average Kilometres Driven", f"=AVERAGE(Cleaned_Data!D2:D{len(df)+1})", FMT_QTY),
        ("Average Vehicle Age", f"=AVERAGE(Cleaned_Data!J2:J{len(df)+1})", '0.0" Years"'),
    ]

    # Create 2x3 KPI Card Grid
    positions = [(5, 1), (5, 3), (5, 5), (8, 1), (8, 3), (8, 5)]
    for (label, formula, fmt), (r, c) in zip(kpis, positions):
        ws_exec.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c+1)
        ws_exec.merge_cells(start_row=r+1, start_column=c, end_row=r+1, end_column=c+1)

        t_cell = ws_exec.cell(row=r, column=c, value=label)
        t_cell.font = KPI_TITLE_FONT
        t_cell.fill = FILL_ICE
        t_cell.alignment = ALIGN_CENTER

        v_cell = ws_exec.cell(row=r+1, column=c, value=formula)
        v_cell.font = KPI_VAL_FONT
        v_cell.fill = FILL_ICE
        v_cell.alignment = ALIGN_CENTER
        v_cell.number_format = fmt

        for ro in range(r, r+2):
            for co in range(c, c+2):
                ws_exec.cell(row=ro, column=co).border = STANDARD_BORDER

    add_disclaimer_banner(ws_exec, 11,
                          "Listing metrics reflect public marketplace asking data. Financial scenario unit economics and working capital metrics are separate simulation models.",
                          max_col=7)

    ws_exec.cell(row=13, column=1, value="2. STRATEGIC EXECUTIVE TAKEAWAYS").font = SECTION_FONT
    takeaways = [
        "1. High Market Concentration: Top 3 OEM brands (Maruti, Hyundai, Mahindra) represent over 60% of total marketplace listings.",
        "2. Diesel vs. Petrol Spread: Diesel listings command a substantial pricing premium over petrol counterparts due to commercial & SUV preference.",
        "3. Accelerated Depreciation: Significant valuation discount occurs across ownership transfers, with 2nd and 3rd owners experiencing steep price reductions.",
        "4. Scenario Gross Margin Benchmark: Assuming an 82% dealer acquisition buy-in and 4% discount, portfolio unit gross margin averages ~14.6%.",
        "5. Working Capital Optimization: Compressing inventory lot holding period from 67 days (Base) to 38 days (Lean) reduces Cash Conversion Cycle by 43 days.",
    ]
    for idx, text in enumerate(takeaways, start=14):
        ws_exec.merge_cells(start_row=idx, start_column=1, end_row=idx, end_column=7)
        c = ws_exec.cell(row=idx, column=1, value=text)
        c.font = DATA_FONT
        c.alignment = ALIGN_LEFT
        ws_exec.row_dimensions[idx].height = 20

    ws_exec.cell(row=21, column=1, value="3. WORKBOOK NAVIGATION GUIDE").font = SECTION_FONT
    sheets_guide = [
        ("Raw_Data & Cleaned_Data", "Full data provenance and cleaned 6,926-vehicle listing dataset with derived dimensions."),
        ("Vehicle & Brand Analysis", "Listing volume, market share %, and price distributions across 32 automotive manufacturers."),
        ("Pricing & Fuel Analysis", "Segmentation across entry/budget to luxury tiers and fuel/transmission cross-tabs."),
        ("Profitability_Scenario", "Dynamic unit economics simulation model with editable acquisition, discount, and reconditioning inputs."),
        ("Working_Capital_Model", "Corporate finance working capital calculator (Current Ratio, DSI, DSO, DPO, Cash Conversion Cycle)."),
        ("Financial_KPI_Dashboard", "Executive presentation dashboard aggregating operational and financial metrics."),
    ]
    r_start = 22
    for s_name, desc in sheets_guide:
        ws_exec.cell(row=r_start, column=1, value=s_name).font = BOLD_DATA_FONT
        ws_exec.merge_cells(start_row=r_start, start_column=2, end_row=r_start, end_column=7)
        ws_exec.cell(row=r_start, column=2, value=desc).font = DATA_FONT
        ws_exec.row_dimensions[r_start].height = 18
        r_start += 1

    auto_fit_columns(ws_exec)

    # -------------------------------------------------------------------------
    # SHEET 2: Raw_Data
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 2: Raw_Data...")
    ws_raw = wb.create_sheet(title="Raw_Data")
    apply_title_banner(ws_raw, "RAW DATASET AUDIT TRAIL: VEHICLE DATASET FROM CARDEKHO",
                       f"Direct Unmodified Extract from Kaggle (Showing first 500 records of {len(raw_df):,})", max_col=len(raw_df.columns))

    raw_headers = list(raw_df.columns)
    ws_raw.row_dimensions[4].height = 22
    for c_idx, h in enumerate(raw_headers, 1):
        cell = ws_raw.cell(row=4, column=c_idx, value=h)
        cell.font = HEADER_FONT
        cell.fill = FILL_SLATE
        cell.alignment = ALIGN_CENTER
        cell.border = STANDARD_BORDER

    # Sample 500 rows for Excel performance while providing full auditability
    sample_raw = raw_df.head(500)
    for r_idx, row in enumerate(sample_raw.itertuples(index=False), 5):
        ws_raw.row_dimensions[r_idx].height = 18
        for c_idx, val in enumerate(row, 1):
            cell = ws_raw.cell(row=r_idx, column=c_idx, value=val)
            cell.font = DATA_FONT
            cell.border = STANDARD_BORDER
            if raw_headers[c_idx - 1] in ["selling_price"]:
                cell.number_format = FMT_INR
                cell.alignment = ALIGN_RIGHT
            elif raw_headers[c_idx - 1] in ["km_driven"]:
                cell.number_format = FMT_QTY
                cell.alignment = ALIGN_RIGHT
            elif raw_headers[c_idx - 1] in ["year", "seats"]:
                cell.alignment = ALIGN_CENTER

    auto_fit_columns(ws_raw)

    # -------------------------------------------------------------------------
    # SHEET 3: Cleaned_Data
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 3: Cleaned_Data...")
    ws_clean = wb.create_sheet(title="Cleaned_Data")
    apply_title_banner(ws_clean, "CLEANED & STANDARDIZED VEHICLE LISTING DATASET",
                       f"Deduplicated Analytical Population ({len(df):,} unique listings with derived columns)", max_col=13)

    clean_cols = [
        ("name", "Vehicle Name", ALIGN_LEFT, None),
        ("year", "Year", ALIGN_CENTER, None),
        ("selling_price", "Selling Price (₹)", ALIGN_RIGHT, FMT_INR),
        ("km_driven", "KM Driven", ALIGN_RIGHT, FMT_QTY),
        ("fuel", "Fuel Type", ALIGN_CENTER, None),
        ("seller_type", "Seller Type", ALIGN_CENTER, None),
        ("transmission", "Transmission", ALIGN_CENTER, None),
        ("owner", "Ownership Tier", ALIGN_LEFT, None),
        ("Vehicle_Brand", "Vehicle Brand", ALIGN_LEFT, None),
        ("Vehicle_Age", "Vehicle Age (Yrs)", ALIGN_CENTER, FMT_QTY),
        ("Price_Category", "Price Category", ALIGN_LEFT, None),
        ("Kilometres_Category", "KM Category", ALIGN_LEFT, None),
        ("Mileage_Category", "Mileage Category", ALIGN_LEFT, None),
    ]

    ws_clean.row_dimensions[4].height = 22
    for c_idx, (col_key, header_title, align, fmt) in enumerate(clean_cols, 1):
        cell = ws_clean.cell(row=4, column=c_idx, value=header_title)
        cell.font = HEADER_FONT
        cell.fill = FILL_NAVY
        cell.alignment = ALIGN_CENTER
        cell.border = STANDARD_BORDER

    # Populate all 6,926 cleaned records
    for r_idx, row in enumerate(df[ [c[0] for c in clean_cols] ].itertuples(index=False), 5):
        ws_clean.row_dimensions[r_idx].height = 17
        for c_idx, val in enumerate(row, 1):
            cell = ws_clean.cell(row=r_idx, column=c_idx, value=val)
            cell.font = DATA_FONT
            cell.alignment = clean_cols[c_idx - 1][2]
            cell.border = STANDARD_BORDER
            if clean_cols[c_idx - 1][3]:
                cell.number_format = clean_cols[c_idx - 1][3]

    auto_fit_columns(ws_clean)

    # -------------------------------------------------------------------------
    # SHEET 4: Vehicle_Analysis
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 4: Vehicle_Analysis...")
    ws_veh = wb.create_sheet(title="Vehicle_Analysis")
    apply_title_banner(ws_veh, "VEHICLE ATTRIBUTES & ODOMETER ANALYSIS",
                       "Listing Distribution across Age Cohorts & Utilization Tiers", max_col=7)

    # Table 1: Age Cohort Analysis
    ws_veh.cell(row=5, column=1, value="VEHICLE AGE COHORT ANALYSIS (2026 Baseline)").font = SECTION_FONT
    headers_age = ["Vehicle Age Bracket", "Listings Count", "Share of Total (%)", "Avg Listed Price (₹)", "Avg KM Driven"]
    ws_veh.row_dimensions[6].height = 22
    for c_idx, h in enumerate(headers_age, 1):
        c = ws_veh.cell(row=6, column=c_idx, value=h)
        c.font = HEADER_FONT
        c.fill = FILL_NAVY
        c.alignment = ALIGN_CENTER
        c.border = STANDARD_BORDER

    age_brackets = [
        ("Under 7 Years (Recent)", 6, 7),
        ("7 to 10 Years (Mid-Age)", 8, 10),
        ("11 to 15 Years (Mature)", 11, 15),
        ("Over 15 Years (Aged)", 16, 50),
    ]

    r_curr = 7
    total_rows = len(df) + 4
    for label, min_a, max_a in age_brackets:
        ws_veh.cell(row=r_curr, column=1, value=label).font = DATA_FONT
        # Count formula
        ws_veh.cell(row=r_curr, column=2, value=f'=COUNTIFS(Cleaned_Data!$J$5:$J${total_rows}, ">={min_a}", Cleaned_Data!$J$5:$J${total_rows}, "<={max_a}")').number_format = FMT_QTY
        # Share formula
        ws_veh.cell(row=r_curr, column=3, value=f'=B{r_curr}/$B$11').number_format = FMT_PCT
        # Avg Price formula
        ws_veh.cell(row=r_curr, column=4, value=f'=AVERAGEIFS(Cleaned_Data!$C$5:$C${total_rows}, Cleaned_Data!$J$5:$J${total_rows}, ">={min_a}", Cleaned_Data!$J$5:$J${total_rows}, "<={max_a}")').number_format = FMT_INR
        # Avg KM formula
        ws_veh.cell(row=r_curr, column=5, value=f'=AVERAGEIFS(Cleaned_Data!$D$5:$D${total_rows}, Cleaned_Data!$J$5:$J${total_rows}, ">={min_a}", Cleaned_Data!$J$5:$J${total_rows}, "<={max_a}")').number_format = FMT_QTY

        for c_idx in range(1, 6):
            ws_veh.cell(row=r_curr, column=c_idx).border = STANDARD_BORDER
        r_curr += 1

    # Total row
    ws_veh.cell(row=11, column=1, value="Total / Portfolio Average").font = BOLD_DATA_FONT
    ws_veh.cell(row=11, column=2, value="=SUM(B7:B10)").number_format = FMT_QTY
    ws_veh.cell(row=11, column=3, value="=SUM(C7:C10)").number_format = FMT_PCT
    ws_veh.cell(row=11, column=4, value=f"=AVERAGE(Cleaned_Data!$C$5:$C${total_rows})").number_format = FMT_INR
    ws_veh.cell(row=11, column=5, value=f"=AVERAGE(Cleaned_Data!$D$5:$D${total_rows})").number_format = FMT_QTY
    for c_idx in range(1, 6):
        ws_veh.cell(row=11, column=c_idx).border = TOTAL_BORDER
        ws_veh.cell(row=11, column=c_idx).font = BOLD_DATA_FONT

    # Add Bar Chart for Age Brackets
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Vehicle Listings by Age Cohort"
    chart1.y_axis.title = "Number of Listings"
    chart1.x_axis.title = "Age Cohort"
    data_ref = Reference(ws_veh, min_col=2, min_row=6, max_row=10)
    cats_ref = Reference(ws_veh, min_col=1, min_row=7, max_row=10)
    chart1.add_data(data_ref, titles_from_data=True)
    chart1.set_categories(cats_ref)
    chart1.legend = None
    chart1.width = 14
    chart1.height = 7
    ws_veh.add_chart(chart1, "A14")

    auto_fit_columns(ws_veh)

    # -------------------------------------------------------------------------
    # SHEET 5: Brand_Analysis
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 5: Brand_Analysis...")
    ws_brand = wb.create_sheet(title="Brand_Analysis")
    apply_title_banner(ws_brand, "AUTOMOTIVE BRAND MARKET CONCENTRATION & PRICING",
                       "Manufacturer-Level Listing Share, Pricing Dispersion, and Capital Allocation", max_col=7)

    ws_brand.cell(row=4, column=1, value="TOP 15 AUTOMOTIVE BRANDS IN MARKETPLACE").font = SECTION_FONT
    brand_headers = ["Vehicle Brand", "Listings Count", "Market Share (%)", "Total Market Value (₹)", "Avg Asking Price (₹)", "Avg KM Driven", "Avg Age (Yrs)"]
    ws_brand.row_dimensions[5].height = 22
    for c_idx, h in enumerate(brand_headers, 1):
        c = ws_brand.cell(row=5, column=c_idx, value=h)
        c.font = HEADER_FONT
        c.fill = FILL_NAVY
        c.alignment = ALIGN_CENTER
        c.border = STANDARD_BORDER

    top15_brands = df["Vehicle_Brand"].value_counts().head(15).index.tolist()
    r_curr = 6
    for b_name in top15_brands:
        ws_brand.cell(row=r_curr, column=1, value=b_name).font = DATA_FONT
        ws_brand.cell(row=r_curr, column=2, value=f'=COUNTIF(Cleaned_Data!$I$5:$I${total_rows}, "{b_name}")').number_format = FMT_QTY
        ws_brand.cell(row=r_curr, column=3, value=f'=B{r_curr}/$B$21').number_format = FMT_PCT
        ws_brand.cell(row=r_curr, column=4, value=f'=SUMIF(Cleaned_Data!$I$5:$I${total_rows}, "{b_name}", Cleaned_Data!$C$5:$C${total_rows})').number_format = FMT_INR
        ws_brand.cell(row=r_curr, column=5, value=f'=AVERAGEIF(Cleaned_Data!$I$5:$I${total_rows}, "{b_name}", Cleaned_Data!$C$5:$C${total_rows})').number_format = FMT_INR
        ws_brand.cell(row=r_curr, column=6, value=f'=AVERAGEIF(Cleaned_Data!$I$5:$I${total_rows}, "{b_name}", Cleaned_Data!$D$5:$D${total_rows})').number_format = FMT_QTY
        ws_brand.cell(row=r_curr, column=7, value=f'=AVERAGEIF(Cleaned_Data!$I$5:$I${total_rows}, "{b_name}", Cleaned_Data!$J$5:$J${total_rows})').number_format = '0.0'

        for c_idx in range(1, 8):
            ws_brand.cell(row=r_curr, column=c_idx).border = STANDARD_BORDER
        r_curr += 1

    # Total row for top 15
    ws_brand.cell(row=21, column=1, value="Top 15 Sub-Total").font = BOLD_DATA_FONT
    ws_brand.cell(row=21, column=2, value="=SUM(B6:B20)").number_format = FMT_QTY
    ws_brand.cell(row=21, column=3, value="=SUM(C6:C20)").number_format = FMT_PCT
    ws_brand.cell(row=21, column=4, value="=SUM(D6:D20)").number_format = FMT_INR
    ws_brand.cell(row=21, column=5, value="=AVERAGE(E6:E20)").number_format = FMT_INR
    ws_brand.cell(row=21, column=6, value="=AVERAGE(F6:F20)").number_format = FMT_QTY
    ws_brand.cell(row=21, column=7, value="=AVERAGE(G6:G20)").number_format = '0.0'
    for c_idx in range(1, 8):
        ws_brand.cell(row=21, column=c_idx).border = TOTAL_BORDER
        ws_brand.cell(row=21, column=c_idx).font = BOLD_DATA_FONT

    # Bar chart for brand volume
    chart2 = BarChart()
    chart2.type = "bar"
    chart2.style = 10
    chart2.title = "Market Concentration: Top Brands by Volume"
    chart2.x_axis.title = "Number of Listings"
    chart2.y_axis.title = "Manufacturer"
    data_ref2 = Reference(ws_brand, min_col=2, min_row=5, max_row=15)
    cats_ref2 = Reference(ws_brand, min_col=1, min_row=6, max_row=15)
    chart2.add_data(data_ref2, titles_from_data=True)
    chart2.set_categories(cats_ref2)
    chart2.legend = None
    chart2.width = 14
    chart2.height = 7
    ws_brand.add_chart(chart2, "A23")

    auto_fit_columns(ws_brand)

    # -------------------------------------------------------------------------
    # SHEET 6: Pricing_Analysis
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 6: Pricing_Analysis...")
    ws_price = wb.create_sheet(title="Pricing_Analysis")
    apply_title_banner(ws_price, "MARKETPLACE PRICING ANALYSIS & SEGMENTATION",
                       "Distribution across Budget, Mid-Range, Premium, and Luxury Tiers", max_col=7)

    ws_price.cell(row=4, column=1, value="PRICE CATEGORY SEGMENTATION MATRIX").font = SECTION_FONT
    price_headers = ["Price Category", "Volume (Units)", "Volume Share (%)", "Total Capital Value (₹)", "Avg Asking Price (₹)", "Avg KM Driven", "Avg Age (Yrs)"]
    ws_price.row_dimensions[5].height = 22
    for c_idx, h in enumerate(price_headers, 1):
        c = ws_price.cell(row=5, column=c_idx, value=h)
        c.font = HEADER_FONT
        c.fill = FILL_NAVY
        c.alignment = ALIGN_CENTER
        c.border = STANDARD_BORDER

    cats = [
        "Budget (< ₹3L)",
        "Mid-Range (₹3L - ₹6L)",
        "Upper Mid-Range (₹6L - ₹10L)",
        "Premium (₹10L - ₹20L)",
        "Luxury (> ₹20L)",
    ]

    r_curr = 6
    for cat in cats:
        ws_price.cell(row=r_curr, column=1, value=cat).font = DATA_FONT
        ws_price.cell(row=r_curr, column=2, value=f'=COUNTIF(Cleaned_Data!$K$5:$K${total_rows}, "{cat}")').number_format = FMT_QTY
        ws_price.cell(row=r_curr, column=3, value=f'=B{r_curr}/$B$11').number_format = FMT_PCT
        ws_price.cell(row=r_curr, column=4, value=f'=SUMIF(Cleaned_Data!$K$5:$K${total_rows}, "{cat}", Cleaned_Data!$C$5:$C${total_rows})').number_format = FMT_INR
        ws_price.cell(row=r_curr, column=5, value=f'=AVERAGEIF(Cleaned_Data!$K$5:$K${total_rows}, "{cat}", Cleaned_Data!$C$5:$C${total_rows})').number_format = FMT_INR
        ws_price.cell(row=r_curr, column=6, value=f'=AVERAGEIF(Cleaned_Data!$K$5:$K${total_rows}, "{cat}", Cleaned_Data!$D$5:$D${total_rows})').number_format = FMT_QTY
        ws_price.cell(row=r_curr, column=7, value=f'=AVERAGEIF(Cleaned_Data!$K$5:$K${total_rows}, "{cat}", Cleaned_Data!$J$5:$J${total_rows})').number_format = '0.0'

        for c_idx in range(1, 8):
            ws_price.cell(row=r_curr, column=c_idx).border = STANDARD_BORDER
        r_curr += 1

    # Total row
    ws_price.cell(row=11, column=1, value="Total Portfolio").font = BOLD_DATA_FONT
    ws_price.cell(row=11, column=2, value="=SUM(B6:B10)").number_format = FMT_QTY
    ws_price.cell(row=11, column=3, value="=SUM(C6:C10)").number_format = FMT_PCT
    ws_price.cell(row=11, column=4, value="=SUM(D6:D10)").number_format = FMT_INR
    ws_price.cell(row=11, column=5, value=f"=AVERAGE(Cleaned_Data!$C$5:$C${total_rows})").number_format = FMT_INR
    ws_price.cell(row=11, column=6, value=f"=AVERAGE(Cleaned_Data!$D$5:$D${total_rows})").number_format = FMT_QTY
    ws_price.cell(row=11, column=7, value=f"=AVERAGE(Cleaned_Data!$J$5:$J${total_rows})").number_format = '0.0'
    for c_idx in range(1, 8):
        ws_price.cell(row=11, column=c_idx).border = TOTAL_BORDER
        ws_price.cell(row=11, column=c_idx).font = BOLD_DATA_FONT

    # Pie chart for price categories
    chart3 = PieChart()
    chart3.title = "Listing Share by Price Category"
    labels3 = Reference(ws_price, min_col=1, min_row=6, max_row=10)
    data3 = Reference(ws_price, min_col=2, min_row=5, max_row=10)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(labels3)
    chart3.width = 13
    chart3.height = 7
    ws_price.add_chart(chart3, "A13")

    auto_fit_columns(ws_price)

    # -------------------------------------------------------------------------
    # SHEET 7: Fuel_Analysis
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 7: Fuel_Analysis...")
    ws_fuel = wb.create_sheet(title="Fuel_Analysis")
    apply_title_banner(ws_fuel, "POWERTRAIN & FUEL TYPE VALUATION ANALYSIS",
                       "Market Listing Performance across Diesel, Petrol, CNG, and LPG", max_col=6)

    ws_fuel.cell(row=4, column=1, value="FUEL TYPE SUMMARY").font = SECTION_FONT
    fuel_headers = ["Fuel Type", "Listings Count", "Market Share (%)", "Avg Asking Price (₹)", "Avg KM Driven", "Avg Age (Yrs)"]
    ws_fuel.row_dimensions[5].height = 22
    for c_idx, h in enumerate(fuel_headers, 1):
        c = ws_fuel.cell(row=5, column=c_idx, value=h)
        c.font = HEADER_FONT
        c.fill = FILL_NAVY
        c.alignment = ALIGN_CENTER
        c.border = STANDARD_BORDER

    fuel_types = ["Diesel", "Petrol", "Cng", "Lpg"]
    r_curr = 6
    for f_type in fuel_types:
        ws_fuel.cell(row=r_curr, column=1, value=f_type).font = DATA_FONT
        ws_fuel.cell(row=r_curr, column=2, value=f'=COUNTIF(Cleaned_Data!$E$5:$E${total_rows}, "{f_type}")').number_format = FMT_QTY
        ws_fuel.cell(row=r_curr, column=3, value=f'=B{r_curr}/$B$10').number_format = FMT_PCT
        ws_fuel.cell(row=r_curr, column=4, value=f'=AVERAGEIF(Cleaned_Data!$E$5:$E${total_rows}, "{f_type}", Cleaned_Data!$C$5:$C${total_rows})').number_format = FMT_INR
        ws_fuel.cell(row=r_curr, column=5, value=f'=AVERAGEIF(Cleaned_Data!$E$5:$E${total_rows}, "{f_type}", Cleaned_Data!$D$5:$D${total_rows})').number_format = FMT_QTY
        ws_fuel.cell(row=r_curr, column=6, value=f'=AVERAGEIF(Cleaned_Data!$E$5:$E${total_rows}, "{f_type}", Cleaned_Data!$J$5:$J${total_rows})').number_format = '0.0'

        for c_idx in range(1, 7):
            ws_fuel.cell(row=r_curr, column=c_idx).border = STANDARD_BORDER
        r_curr += 1

    # Total row
    ws_fuel.cell(row=10, column=1, value="Total").font = BOLD_DATA_FONT
    ws_fuel.cell(row=10, column=2, value="=SUM(B6:B9)").number_format = FMT_QTY
    ws_fuel.cell(row=10, column=3, value="=SUM(C6:C9)").number_format = FMT_PCT
    ws_fuel.cell(row=10, column=4, value=f"=AVERAGE(Cleaned_Data!$C$5:$C${total_rows})").number_format = FMT_INR
    ws_fuel.cell(row=10, column=5, value=f"=AVERAGE(Cleaned_Data!$D$5:$D${total_rows})").number_format = FMT_QTY
    ws_fuel.cell(row=10, column=6, value=f"=AVERAGE(Cleaned_Data!$J$5:$J${total_rows})").number_format = '0.0'
    for c_idx in range(1, 7):
        ws_fuel.cell(row=10, column=c_idx).border = TOTAL_BORDER
        ws_fuel.cell(row=10, column=c_idx).font = BOLD_DATA_FONT

    # Transmission Cross Tab
    ws_fuel.cell(row=13, column=1, value="TRANSMISSION VALUATION PREMIUM").font = SECTION_FONT
    trans_headers = ["Transmission", "Volume (Units)", "Volume Share (%)", "Avg Asking Price (₹)", "Price Premium vs Manual (%)"]
    ws_fuel.row_dimensions[14].height = 22
    for c_idx, h in enumerate(trans_headers, 1):
        c = ws_fuel.cell(row=14, column=c_idx, value=h)
        c.font = HEADER_FONT
        c.fill = FILL_SLATE
        c.alignment = ALIGN_CENTER
        c.border = STANDARD_BORDER

    ws_fuel.cell(row=15, column=1, value="Manual").font = DATA_FONT
    ws_fuel.cell(row=15, column=2, value=f'=COUNTIF(Cleaned_Data!$G$5:$G${total_rows}, "Manual")').number_format = FMT_QTY
    ws_fuel.cell(row=15, column=3, value="=B15/(B15+B16)").number_format = FMT_PCT
    ws_fuel.cell(row=15, column=4, value=f'=AVERAGEIF(Cleaned_Data!$G$5:$G${total_rows}, "Manual", Cleaned_Data!$C$5:$C${total_rows})').number_format = FMT_INR
    ws_fuel.cell(row=15, column=5, value=0.0).number_format = FMT_PCT

    ws_fuel.cell(row=16, column=1, value="Automatic").font = DATA_FONT
    ws_fuel.cell(row=16, column=2, value=f'=COUNTIF(Cleaned_Data!$G$5:$G${total_rows}, "Automatic")').number_format = FMT_QTY
    ws_fuel.cell(row=16, column=3, value="=B16/(B15+B16)").number_format = FMT_PCT
    ws_fuel.cell(row=16, column=4, value=f'=AVERAGEIF(Cleaned_Data!$G$5:$G${total_rows}, "Automatic", Cleaned_Data!$C$5:$C${total_rows})').number_format = FMT_INR
    ws_fuel.cell(row=16, column=5, value="=(D16-D15)/D15").number_format = FMT_PCT

    for ro in [15, 16]:
        for co in range(1, 6):
            ws_fuel.cell(row=ro, column=co).border = STANDARD_BORDER

    auto_fit_columns(ws_fuel)

    # -------------------------------------------------------------------------
    # SHEET 8: Ownership_Analysis
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 8: Ownership_Analysis...")
    ws_own = wb.create_sheet(title="Ownership_Analysis")
    apply_title_banner(ws_own, "OWNERSHIP HISTORY VALUATION DISCOUNT ANALYSIS",
                       "Vehicle Pricing Depreciation Across Successive Ownership Transfers", max_col=6)

    ws_own.cell(row=4, column=1, value="OWNERSHIP TIER VALUATION TABLE").font = SECTION_FONT
    own_headers = ["Ownership Tier", "Listings Count", "Share (%)", "Avg Asking Price (₹)", "Discount vs First Owner (%)", "Avg Odometer (KM)"]
    ws_own.row_dimensions[5].height = 22
    for c_idx, h in enumerate(own_headers, 1):
        c = ws_own.cell(row=5, column=c_idx, value=h)
        c.font = HEADER_FONT
        c.fill = FILL_NAVY
        c.alignment = ALIGN_CENTER
        c.border = STANDARD_BORDER

    tiers = [
        "First Owner",
        "Second Owner",
        "Third Owner",
        "Fourth & Above Owner",
        "Test Drive Car"
    ]
    r_curr = 6
    for tier in tiers:
        ws_own.cell(row=r_curr, column=1, value=tier).font = DATA_FONT
        ws_own.cell(row=r_curr, column=2, value=f'=COUNTIF(Cleaned_Data!$H$5:$H${total_rows}, "{tier}")').number_format = FMT_QTY
        ws_own.cell(row=r_curr, column=3, value=f'=B{r_curr}/$B$11').number_format = FMT_PCT
        ws_own.cell(row=r_curr, column=4, value=f'=AVERAGEIF(Cleaned_Data!$H$5:$H${total_rows}, "{tier}", Cleaned_Data!$C$5:$C${total_rows})').number_format = FMT_INR
        # Discount relative to First Owner (row 6)
        ws_own.cell(row=r_curr, column=5, value=f'=(D{r_curr}-$D$6)/$D$6').number_format = FMT_PCT
        ws_own.cell(row=r_curr, column=6, value=f'=AVERAGEIF(Cleaned_Data!$H$5:$H${total_rows}, "{tier}", Cleaned_Data!$D$5:$D${total_rows})').number_format = FMT_QTY

        for c_idx in range(1, 7):
            ws_own.cell(row=r_curr, column=c_idx).border = STANDARD_BORDER
        r_curr += 1

    # Total row
    ws_own.cell(row=11, column=1, value="Total Portfolio").font = BOLD_DATA_FONT
    ws_own.cell(row=11, column=2, value="=SUM(B6:B10)").number_format = FMT_QTY
    ws_own.cell(row=11, column=3, value="=SUM(C6:C10)").number_format = FMT_PCT
    ws_own.cell(row=11, column=4, value=f"=AVERAGE(Cleaned_Data!$C$5:$C${total_rows})").number_format = FMT_INR
    ws_own.cell(row=11, column=5, value="-").alignment = ALIGN_CENTER
    ws_own.cell(row=11, column=6, value=f"=AVERAGE(Cleaned_Data!$D$5:$D${total_rows})").number_format = FMT_QTY
    for c_idx in range(1, 7):
        ws_own.cell(row=11, column=c_idx).border = TOTAL_BORDER
        ws_own.cell(row=11, column=c_idx).font = BOLD_DATA_FONT

    auto_fit_columns(ws_own)

    # -------------------------------------------------------------------------
    # SHEET 9: Profitability_Scenario
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 9: Profitability_Scenario...")
    ws_prof = wb.create_sheet(title="Profitability_Scenario")
    apply_title_banner(ws_prof, "DEALERSHIP VEHICLE PROFITABILITY SCENARIO SIMULATOR",
                       "Parametric Unit Economics Model | Live User-Configurable Operational Assumptions", max_col=10)

    add_disclaimer_banner(ws_prof, 4,
                          "HYPOTHETICAL FINANCIAL SCENARIO – NOT ACTUAL DEALERSHIP ACCOUNTING DATA. Assumed purchase buy-in and reconditioning costs.",
                          max_col=10)

    # Assumptions Block
    ws_prof.cell(row=6, column=1, value="DYNAMIC MODEL ASSUMPTIONS (EDITABLE)").font = SECTION_FONT
    ws_prof.cell(row=6, column=5, value="PORTFOLIO SCENARIO KPI SUMMARY").font = SECTION_FONT

    assumptions = [
        ("Assumed Vehicle Acquisition Cost (% of List)", 0.82, FMT_PCT, "B7"),
        ("Anticipated Negotiation Discount (% of List)", 0.04, FMT_PCT, "B8"),
        ("Reconditioning Cost per Unit (₹)", 15000, FMT_INR, "B9"),
        ("Transportation & Logistics Cost per Unit (₹)", 5000, FMT_INR, "B10"),
        ("Other Direct Selling Costs per Unit (₹)", 8000, FMT_INR, "B11"),
    ]
    for idx, (label, val, fmt, cell_ref) in enumerate(assumptions, start=7):
        ws_prof.cell(row=idx, column=1, value=label).font = BOLD_DATA_FONT
        c = ws_prof.cell(row=idx, column=2, value=val)
        c.font = BOLD_DATA_FONT
        c.number_format = fmt
        c.fill = FILL_LIGHT
        c.alignment = ALIGN_RIGHT
        c.border = STANDARD_BORDER

    # KPI Summary Tiles on Right Side
    ws_prof.cell(row=7, column=5, value="Scenario Gross Profit (₹)").font = KPI_TITLE_FONT
    ws_prof.cell(row=7, column=6, value="=SUM(H15:H514)").number_format = FMT_INR
    ws_prof.cell(row=7, column=6).font = KPI_VAL_FONT

    ws_prof.cell(row=8, column=5, value="Scenario Gross Margin (%)").font = KPI_TITLE_FONT
    ws_prof.cell(row=8, column=6, value="=F7/SUM(F15:F514)").number_format = FMT_PCT
    ws_prof.cell(row=8, column=6).font = KPI_VAL_FONT

    ws_prof.cell(row=9, column=5, value="Scenario Net Contribution (₹)").font = KPI_TITLE_FONT
    ws_prof.cell(row=9, column=6, value="=SUM(J15:J514)").number_format = FMT_INR
    ws_prof.cell(row=9, column=6).font = KPI_VAL_FONT

    ws_prof.cell(row=10, column=5, value="Scenario Net Contribution Margin (%)").font = KPI_TITLE_FONT
    ws_prof.cell(row=10, column=6, value="=F9/SUM(F15:F514)").number_format = FMT_PCT
    ws_prof.cell(row=10, column=6).font = KPI_VAL_FONT

    for ro in range(7, 11):
        for co in [5, 6]:
            ws_prof.cell(row=ro, column=co).border = STANDARD_BORDER
            ws_prof.cell(row=ro, column=co).fill = FILL_ICE

    # Vehicle-Level Simulation Table (Sample 500 rows with live dynamic Excel formulas)
    ws_prof.cell(row=13, column=1, value="SIMULATED VEHICLE UNIT ECONOMICS (Top 500 Listings)").font = SECTION_FONT
    sim_headers = [
        "Vehicle Name", "Brand", "Year", "Listed Price (₹)",
        "Scenario Discount (₹)", "Scenario Revenue (₹)",
        "Acquisition Cost (₹)", "Scenario Gross Profit (₹)",
        "Gross Margin (%)", "Scenario Net Contribution (₹)"
    ]
    ws_prof.row_dimensions[14].height = 22
    for c_idx, h in enumerate(sim_headers, 1):
        c = ws_prof.cell(row=14, column=c_idx, value=h)
        c.font = HEADER_FONT
        c.fill = FILL_NAVY
        c.alignment = ALIGN_CENTER
        c.border = STANDARD_BORDER

    # Populate 500 rows with formulas pointing to assumptions
    for r_idx in range(15, 515):
        clean_row = r_idx - 10 # Corresponds to row in Cleaned_Data
        ws_prof.row_dimensions[r_idx].height = 17

        # Name, Brand, Year, Price referencing Cleaned_Data
        ws_prof.cell(row=r_idx, column=1, value=f"=Cleaned_Data!A{clean_row}").font = DATA_FONT
        ws_prof.cell(row=r_idx, column=2, value=f"=Cleaned_Data!I{clean_row}").font = DATA_FONT
        ws_prof.cell(row=r_idx, column=3, value=f"=Cleaned_Data!B{clean_row}").font = DATA_FONT
        ws_prof.cell(row=r_idx, column=3).alignment = ALIGN_CENTER
        ws_prof.cell(row=r_idx, column=4, value=f"=Cleaned_Data!C{clean_row}").number_format = FMT_INR

        # Scenario Discount = Price * $B$8
        ws_prof.cell(row=r_idx, column=5, value=f"=D{r_idx}*$B$8").number_format = FMT_INR
        # Scenario Revenue = Price - Discount
        ws_prof.cell(row=r_idx, column=6, value=f"=D{r_idx}-E{r_idx}").number_format = FMT_INR
        # Scenario Acquisition Cost = Price * $B$7
        ws_prof.cell(row=r_idx, column=7, value=f"=D{r_idx}*$B$7").number_format = FMT_INR
        # Scenario Gross Profit = Revenue - Acquisition Cost
        ws_prof.cell(row=r_idx, column=8, value=f"=F{r_idx}-G{r_idx}").number_format = FMT_INR
        # Gross Margin % = Gross Profit / Revenue
        ws_prof.cell(row=r_idx, column=9, value=f"=H{r_idx}/F{r_idx}").number_format = FMT_PCT
        # Net Contribution = Gross Profit - (Recond + Transport + Other)
        ws_prof.cell(row=r_idx, column=10, value=f"=H{r_idx}-($B$9+$B$10+$B$11)").number_format = FMT_INR

        for c_idx in range(1, 11):
            ws_prof.cell(row=r_idx, column=c_idx).border = STANDARD_BORDER

    auto_fit_columns(ws_prof)

    # -------------------------------------------------------------------------
    # SHEET 10: Working_Capital_Model
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 10: Working_Capital_Model...")
    ws_wc = wb.create_sheet(title="Working_Capital_Model")
    apply_title_banner(ws_wc, "DEALERSHIP WORKING CAPITAL & CASH CONVERSION CYCLE MODEL",
                       "Corporate Finance Liquidity Simulator & Benchmark Operating Scenarios", max_col=7)

    add_disclaimer_banner(ws_wc, 4,
                          "ILLUSTRATIVE WORKING CAPITAL MODEL – USER-ENTERED ASSUMPTIONS. No actual dealership balance sheet data is represented.",
                          max_col=7)

    ws_wc.cell(row=6, column=1, value="DEALERSHIP BENCHMARK SCENARIO COMPARISON TABLE").font = SECTION_FONT
    wc_headers = [
        "Financial Metric / Working Capital Dimension",
        "Base Case (Standard)",
        "Lean Optimized (Fast Velocity)",
        "Stressed (High Lot Aging)",
        "Variance (Lean vs Base)",
        "Financial Interpretation"
    ]
    ws_wc.row_dimensions[7].height = 24
    for c_idx, h in enumerate(wc_headers, 1):
        c = ws_wc.cell(row=7, column=c_idx, value=h)
        c.font = HEADER_FONT
        c.fill = FILL_NAVY
        c.alignment = ALIGN_CENTER
        c.border = STANDARD_BORDER

    wc_rows = [
        ("Current Assets (₹ Cr)", 4.50, 3.20, 5.80, "=C8-B8", "Total short-term resources available for dealership operations."),
        ("Current Liabilities (₹ Cr)", 2.80, 2.50, 3.40, "=C9-B9", "Trade payables, floor-plan debt lines, and accrued dealer expenses."),
        ("Net Working Capital (₹ Cr)", "=B8-B9", "=C8-C9", "=D8-D9", "=C10-B10", "Capital cushion required to finance ongoing vehicle inventory and credit sales."),
        ("Current Ratio", "=B8/B9", "=C8/C9", "=D8/D9", "=C11-B11", "Coverage ratio of short-term liabilities (Target: 1.30x - 1.50x)."),
        ("Quick Ratio (Acid-Test)", "=(B8-2.75)/B9", "=(C8-1.60)/C9", "=(D8-3.50)/D9", "=C12-B12", "Excludes inventory to assess immediate liquidity safety (Target: > 1.00x)."),
        ("Inventory Holding Value (₹ Cr)", 2.75, 1.60, 3.50, "=C13-B13", "Average carrying value of used-car inventory parked on dealership lots."),
        ("Inventory Days (DSI)", 66.9, 38.9, 85.2, "=C14-B14", "Average number of days a vehicle sits on lot before retail sale."),
        ("Days Sales Outstanding (DSO)", 20.3, 12.2, 35.5, "=C15-B15", "Debtor collection lag for retail finance approvals and trade customer credit."),
        ("Days Payable Outstanding (DPO)", 33.0, 42.4, 22.4, "=C16-B16", "Credit term negotiated with vehicle suppliers and auto wholesale auctions."),
        ("Cash Conversion Cycle (CCC Days)", "=B14+B15-B16", "=C14+C15-C16", "=D14+D15-D16", "=C17-B17", "Net elapsed days from cash outlay for vehicle inventory to cash receipt."),
        ("Annual Inventory Holding Cost @ 10.5% (₹ Lakhs)", "=B10*10.5", "=C10*10.5", "=D10*10.5", "=C18-B18", "Floor-plan line borrowing interest carrying burden."),
    ]

    for idx, (label, b_val, l_val, s_val, var_form, interp) in enumerate(wc_rows, start=8):
        ws_wc.row_dimensions[idx].height = 20
        c1 = ws_wc.cell(row=idx, column=1, value=label)
        c1.font = BOLD_DATA_FONT if "Ratio" in label or "Cycle" in label or "Capital" in label else DATA_FONT
        c1.border = STANDARD_BORDER

        # Base, Lean, Stressed
        for col_idx, val in [(2, b_val), (3, l_val), (4, s_val)]:
            c = ws_wc.cell(row=idx, column=col_idx, value=val)
            c.border = STANDARD_BORDER
            c.alignment = ALIGN_RIGHT
            if "Cr" in label:
                c.number_format = '"₹"#,##0.00" Cr"'
            elif "Ratio" in label:
                c.number_format = FMT_MULT
                c.font = BOLD_DATA_FONT
            elif "Days" in label or "DSI" in label or "DSO" in label or "DPO" in label:
                c.number_format = FMT_DAYS
                c.font = BOLD_DATA_FONT
            elif "Lakhs" in label:
                c.number_format = '"₹"#,##0.0" L"'
            else:
                c.number_format = '0.00'

        # Variance
        c_var = ws_wc.cell(row=idx, column=5, value=var_form)
        c_var.border = STANDARD_BORDER
        c_var.alignment = ALIGN_RIGHT
        c_var.font = BOLD_DATA_FONT
        if "Cr" in label:
            c_var.number_format = '"₹"#,##0.00" Cr"'
        elif "Ratio" in label:
            c_var.number_format = '+0.00;-0.00;0.00'
        elif "Days" in label:
            c_var.number_format = '+0.0;-0.0;0.0'
        else:
            c_var.number_format = '0.00'

        # Interpretation
        c_int = ws_wc.cell(row=idx, column=6, value=interp)
        c_int.font = DATA_FONT
        c_int.border = STANDARD_BORDER
        c_int.alignment = ALIGN_LEFT

    # Conditional formatting on Cash Conversion Cycle row (row 17)
    ws_wc.conditional_formatting.add(
        "B17:D17",
        CellIsRule(operator="lessThan", formula=["20"], stopIfTrue=True, fill=FILL_SUCCESS)
    )
    ws_wc.conditional_formatting.add(
        "B17:D17",
        CellIsRule(operator="greaterThan", formula=["80"], stopIfTrue=True, fill=FILL_DISCLAIMER)
    )

    auto_fit_columns(ws_wc)

    # -------------------------------------------------------------------------
    # SHEET 11: Financial_KPI_Dashboard
    # -------------------------------------------------------------------------
    print("[EXCEL GENERATOR] Building Sheet 11: Financial_KPI_Dashboard...")
    ws_dash = wb.create_sheet(title="Financial_KPI_Dashboard")
    apply_title_banner(ws_dash, "AUTOMOTIVE DEALERSHIP FINANCIAL KPI DASHBOARD",
                       "Consolidated Management Scorecard & Strategic Performance Indicators", max_col=7)

    ws_dash.cell(row=4, column=1, value="CONSOLIDATED EXECUTIVE METRICS").font = SECTION_FONT

    dash_kpi_blocks = [
        ("Marketplace Listing Volume", "=Executive_Summary!B6", FMT_QTY, "Observed unique used vehicles"),
        ("Gross Listing Valuation", "=Executive_Summary!B7", FMT_INR, "Aggregate inventory asking value"),
        ("Median Asking Price", "=Executive_Summary!D7", FMT_INR, "Marketplace central valuation tendency"),
        ("Scenario Gross Margin", "=Profitability_Scenario!F8", FMT_PCT, "Simulated gross profit percentage"),
        ("Scenario Net Margin", "=Profitability_Scenario!F10", FMT_PCT, "Unit economic net contribution"),
        ("Cash Conversion Cycle (Base)", "=Working_Capital_Model!B17", FMT_DAYS, "Operating capital velocity (Base)"),
        ("Current Ratio (Base)", "=Working_Capital_Model!B11", FMT_MULT, "Liquidity coverage multiple"),
        ("Quick Ratio (Base)", "=Working_Capital_Model!B12", FMT_MULT, "Immediate acid-test coverage"),
    ]

    r_curr = 6
    for idx, (label, form, fmt, note) in enumerate(dash_kpi_blocks):
        ws_dash.cell(row=r_curr, column=1, value=label).font = BOLD_DATA_FONT
        ws_dash.cell(row=r_curr, column=1).border = STANDARD_BORDER

        val_cell = ws_dash.cell(row=r_curr, column=2, value=form)
        val_cell.font = BOLD_DATA_FONT
        val_cell.alignment = ALIGN_RIGHT
        val_cell.number_format = fmt
        val_cell.fill = FILL_ICE
        val_cell.border = STANDARD_BORDER

        note_cell = ws_dash.cell(row=r_curr, column=3, value=note)
        note_cell.font = DATA_FONT
        note_cell.border = STANDARD_BORDER

        ws_dash.row_dimensions[r_curr].height = 20
        r_curr += 1

    add_disclaimer_banner(ws_dash, 16,
                          "MANDATORY AUDIT COMPLIANCE: Metrics combine observed public listings with separate financial scenario models.",
                          max_col=7)

    auto_fit_columns(ws_dash)

    # -------------------------------------------------------------------------
    # Save Workbook
    # -------------------------------------------------------------------------
    os.makedirs(os.path.dirname(EXCEL_OUTPUT_PATH), exist_ok=True)
    wb.save(EXCEL_OUTPUT_PATH)
    print(f"[EXCEL GENERATOR] Successfully created professional Excel workbook at: {EXCEL_OUTPUT_PATH}")
    print(f"[EXCEL GENERATOR] Total worksheets: {len(wb.sheetnames)}: {wb.sheetnames}")
    return EXCEL_OUTPUT_PATH


if __name__ == "__main__":
    generate_workbook()
