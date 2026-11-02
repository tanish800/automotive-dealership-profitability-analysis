# PROJECT LIMITATIONS & METHODOLOGICAL BOUNDARIES

**Project Title:** Automotive Dealership Profitability & Working Capital Analysis  
**Repository Name:** `automotive-dealership-profitability-analysis`  
**Auditor / Author:** Senior Financial Analyst & Automotive Industry Consultant  

---

## 1. Context & Purpose of Limitations Disclosure

In institutional financial analysis and corporate consulting, transparently documenting analytical boundaries is mandatory. This document details the structural, operational, and data limitations of this study to prevent misinterpretation of findings.

---

## 2. Structural Dataset Limitations

### 2.1 Asking Prices vs. Verified Transaction Invoices
- **Observation:** The CarDekho dataset contains **advertised listing prices (asking prices)** posted on a public digital marketplace.
- **Limitation:** In the used-car retail market, negotiated final transaction prices typically involve a discount or trade-in adjustment.
- **Analytical Mitigation:** Our unit economics model introduces an explicit, editable **4.0% negotiation markdown buffer** (`Scenario_Discount`) to approximate realized transaction revenue.

### 2.2 Absence of Purchase Costs & COGS
- **Observation:** The public dataset contains zero records of original dealer wholesale acquisition costs, auction buy-in fees, or trade-in valuations.
- **Limitation:** Actual gross profit cannot be calculated from raw dataset columns alone without making arbitrary fabrications.
- **Analytical Mitigation:** We implemented a separate **Parametric Unit Economics Simulation Model** (`ProfitabilityScenarioModel`) with user-configurable buy-in assumptions (82% default) and clearly stamped every resulting metric as `HYPOTHETICAL FINANCIAL SCENARIO`.

### 2.3 Cross-Sectional Snapshot vs. Longitudinal History
- **Observation:** The dataset represents a point-in-time marketplace scrape rather than a chronological stock register with time-stamped stock-in and stock-out dates.
- **Limitation:** Actual vehicle holding periods, seasonal turnover peaks, and historical stock movements cannot be directly measured from listing timestamps.
- **Analytical Mitigation:** Vehicle Age was rigorously calculated using the current calendar baseline (2026), and working capital velocity (DSI, DSO, DPO) was evaluated using corporate finance scenario models based on benchmark dealership financial statements.

---

## 3. Financial Modeling Boundaries

### 3.1 Illustrative Working Capital Assumptions
- **Observation:** The real CarDekho dataset does not include dealership balance sheets, accounts receivable aging schedules, trade creditor ledgers, or floor-plan line agreements.
- **Limitation:** Working capital metrics (Current Ratio, Quick Ratio, DSO, DPO, CCC) cannot be ascribed to CarDekho as an operating enterprise or to any specific franchise dealership.
- **Analytical Mitigation:** All working capital calculations are segregated in an interactive corporate finance calculator with three standardized industry benchmarks (Base Case, Lean Optimized, Stressed Case) and labeled `ILLUSTRATIVE WORKING CAPITAL MODEL – USER-ENTERED ASSUMPTIONS`.

### 3.2 Fixed Unit Operating Expense Allocations
- **Observation:** Reconditioning (₹15,000), transport (₹5,000), and selling costs (₹8,000) are modeled as fixed baseline allocations per unit.
- **Limitation:** In commercial dealership operations, reconditioning costs vary significantly based on vehicle age, odometer mileage, and mechanical condition (e.g. an 8-year-old diesel SUV may require ₹35,000 in suspension and tire repairs, whereas a 2-year-old hatchback requires only ₹8,000 in cosmetic detailing).
- **Analytical Mitigation:** The financial scenario calculator provides full parameter flexibility, allowing users to modify direct cost inputs dynamically.

---

## 4. Conclusion & Audit Compliance Statement

By establishing a clear, auditable boundary between **empirical dataset observations** and **hypothetical scenario modeling**, this project adheres to the highest standards of corporate finance governance, ensuring data integrity without synthetic fabrication.
