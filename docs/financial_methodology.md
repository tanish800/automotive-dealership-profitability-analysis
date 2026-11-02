# FINANCIAL METHODOLOGY & KPI DEFINITIONS SPECIFICATION

**Project Title:** Automotive Dealership Profitability & Working Capital Analysis  
**Repository Name:** `automotive-dealership-profitability-analysis`  
**Target Profile:** B.Com + MBA Finance (Financial Analyst / FP&A / Business Operations)

---

## 1. Overview of Analytical Framework

Automotive dealership finance operates on two interconnected financial pillars:
1. **Unit Economics & Gross Profitability (P&L Optimization):** Maximizing the net dollar spread between vehicle retail selling price and total landed vehicle cost (wholesale acquisition, reconditioning, freight, and sales commissions).
2. **Working Capital & Liquidity Management (Balance Sheet Velocity):** Minimizing the Cash Conversion Cycle (CCC) and floor-plan interest carrying drag by accelerating vehicle lot turn (DSI) and debtor collections (DSO) while negotiating sound supplier credit terms (DPO).

---

## 2. Unit Economics Scenario Modeling (Phase 5)

Because the public CarDekho dataset provides listed asking prices (`selling_price`) but no confidential dealership wholesale purchase invoices, we employ a parameterized scenario simulation model:

### 2.1 Assumptions & Parameters
- **Expected Selling Price ($P$):** Listed vehicle selling price.
- **Negotiation Discount Rate ($d$):** 4.0% expected markdown at closing (configurable 0% - 10%).
- **Acquisition Buy-In Rate ($a$):** 82.0% of listed price assumed purchase price (configurable 70% - 90%).
- **Reconditioning Cost ($C_{recond}$):** ₹15,000 per unit (mechanical servicing, detailing, tires).
- **Logistics & Freight ($C_{trans}$):** ₹5,000 per unit (flatbed transport from auction/trade-in).
- **Other Direct Selling Expenses ($C_{other}$):** ₹8,000 per unit (documentation, detailing, sales commission).

### 2.2 Mathematical Formulations
$$\text{Scenario Revenue} = P \times (1 - d)$$

$$\text{Scenario Acquisition Cost (COGS)} = P \times a$$

$$\text{Scenario Gross Profit} = \text{Scenario Revenue} - \text{Scenario Acquisition Cost}$$

$$\text{Scenario Gross Margin (\%)} = \left(\frac{\text{Scenario Gross Profit}}{\text{Scenario Revenue}}\right) \times 100$$

$$\text{Scenario Direct Costs} = C_{recond} + C_{trans} + C_{other} = ₹28,000$$

$$\text{Scenario Net Contribution} = \text{Scenario Gross Profit} - \text{Scenario Direct Costs}$$

$$\text{Scenario Net Margin (\%)} = \left(\frac{\text{Scenario Net Contribution}}{\text{Scenario Revenue}}\right) \times 100$$

---

## 3. Corporate Working Capital Scenario Framework (Phase 7)

Working capital reflects the operating liquidity required by an automotive dealership to finance vehicle inventory parked on the lot and customer receivables before payment is received.

### 3.1 Balance Sheet Components
- **Cash and Bank Balances ($C$):** Unrestricted dealership operating cash.
- **Accounts Receivable ($AR$):** Customer financing payouts pending from retail banks, captive auto financiers, and corporate trade receivables.
- **Inventory Carrying Value ($Inv$):** Wholesale book value of vehicles parked on dealer lots awaiting retail sale.
- **Other Current Assets ($OCA$):** Prepaid taxes, vendor deposits, insurance advances.
- **Accounts Payable ($AP$):** Open trade payables owed to wholesale auctions, private trade-in sellers, and parts suppliers.
- **Short-Term Borrowings ($STD$):** Floor-plan line of credit utilized to finance vehicle inventory.
- **Other Current Liabilities ($OCL$):** Accrued dealer payroll, customer earnest deposits, sales taxes payable.

### 3.2 Liquidity Ratios & Cash Conversion Cycle Formulas

#### Net Working Capital (NWC)
$$\text{Net Working Capital} = \text{Total Current Assets} - \text{Total Current Liabilities}$$

#### Current Ratio
$$\text{Current Ratio} = \frac{\text{Total Current Assets}}{\text{Total Current Liabilities}}$$
*Dealership Benchmark:* $1.30x - 1.50x$. Multiples below $1.10x$ signal short-term liquidity strain; multiples above $2.0x$ reflect excess idle capital trapped in aged inventory.

#### Quick Ratio (Acid-Test Ratio)
$$\text{Quick Ratio} = \frac{\text{Total Current Assets} - \text{Inventory}}{\text{Total Current Liabilities}}$$
*Dealership Benchmark:* $0.60x - 0.80x$ (Automotive retail is naturally inventory-intensive; cash and receivables provide the primary immediate coverage).

#### Inventory Turnover Ratio
$$\text{Inventory Turnover} = \frac{\text{Annual Cost of Goods Sold (COGS)}}{\text{Average Inventory Value}}$$
*Dealership Benchmark:* $6.0x - 9.0x$ annual turns.

#### Days Sales of Inventory (DSI / DIO)
$$\text{DSI} = \left(\frac{\text{Average Inventory}}{\text{Annual COGS}}\right) \times 365$$
*Dealership Benchmark:* Target $< 45 \text{ days}$. Each day a vehicle sits on a dealer lot beyond 45 days increases depreciation risk and floor-plan interest burden.

#### Days Sales Outstanding (DSO)
$$\text{DSO} = \left(\frac{\text{Average Accounts Receivable}}{\text{Annual Credit Sales}}\right) \times 365$$
*Dealership Benchmark:* $12 - 20 \text{ days}$. Driven by bank financing disbursal efficiency.

#### Days Payable Outstanding (DPO)
$$\text{DPO} = \left(\frac{\text{Average Accounts Payable}}{\text{Annual Credit Purchases}}\right) \times 365$$
*Dealership Benchmark:* $30 - 45 \text{ days}$. Represents trade credit terms negotiated with auto auctions and suppliers.

#### Cash Conversion Cycle (CCC)
$$\text{Cash Conversion Cycle} = \text{DSI} + \text{DSO} - \text{DPO}$$
*Financial Interpretation:* The net number of days capital remains tied up in operations from cash payment for vehicle purchase until cash collection from retail sale. Shorter cycles liberate liquidity for inventory replenishment without external borrowing.

#### Annual Floor-Plan Carrying Drag
$$\text{Annual Carrying Cost} = \max(0, \text{NWC}) \times \text{Cost of Debt (\%)} = \text{NWC} \times 10.5\%$$
*Financial Interpretation:* The direct annual financing interest expense incurred on capital tied up in working capital.
