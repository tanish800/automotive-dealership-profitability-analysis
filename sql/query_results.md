# AutoFinance Analytics: SQL Business Query Execution Results

### Query 1
```sql
SELECT 
    v.Brand,
    v.Model,
    v.Vehicle_Category,
    SUM(s.Quantity) AS Total_Units_Sold,
    ROUND(SUM(s.Total_Revenue), 2) AS Total_Revenue_INR,
    ROUND(AVG(s.Selling_Price), 2) AS Avg_Selling_Price_INR
FROM sales_data s
JOIN vehicle_master v ON s.Vehicle_ID = v.Vehicle_ID
GROUP BY v.Brand, v.Model, v.Vehicle_Category
ORDER BY Total_Revenue_INR DESC
LIMIT 10;

-- ----------------------------------------------------------------------
-- QUERY 2: Top 10 Vehicles by Gross Profit
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 2
```sql
SELECT 
    v.Brand,
    v.Model,
    v.Vehicle_Category,
    SUM(s.Quantity) AS Units_Sold,
    ROUND(SUM(s.Total_Revenue), 2) AS Total_Revenue_INR,
    ROUND(SUM(s.Vehicle_Cost), 2) AS Total_Cost_INR,
    ROUND(SUM(s.Gross_Profit), 2) AS Total_Gross_Profit_INR,
    ROUND((SUM(s.Gross_Profit) * 100.0) / SUM(s.Total_Revenue), 2) AS Gross_Margin_Pct
FROM sales_data s
JOIN vehicle_master v ON s.Vehicle_ID = v.Vehicle_ID
GROUP BY v.Brand, v.Model, v.Vehicle_Category
ORDER BY Total_Gross_Profit_INR DESC
LIMIT 10;

-- ----------------------------------------------------------------------
-- QUERY 3: Lowest-Margin Vehicle Models
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 3
```sql
SELECT 
    v.Brand,
    v.Model,
    v.Vehicle_Category,
    SUM(s.Quantity) AS Units_Sold,
    ROUND(AVG(s.Discount_Pct), 2) AS Avg_Discount_Pct,
    ROUND(SUM(s.Total_Revenue), 2) AS Total_Revenue_INR,
    ROUND(SUM(s.Gross_Profit), 2) AS Total_Gross_Profit_INR,
    ROUND((SUM(s.Gross_Profit) * 100.0) / SUM(s.Total_Revenue), 2) AS Gross_Margin_Pct
FROM sales_data s
JOIN vehicle_master v ON s.Vehicle_ID = v.Vehicle_ID
GROUP BY v.Brand, v.Model, v.Vehicle_Category
HAVING SUM(s.Quantity) >= 15
ORDER BY Gross_Margin_Pct ASC
LIMIT 5;

-- ----------------------------------------------------------------------
-- QUERY 4: Monthly Revenue Trends (24-Month Trajectory)
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 4
```sql
SELECT 
    Year_Month,
    COUNT(Sale_ID) AS Total_Transactions,
    SUM(Quantity) AS Total_Units_Sold,
    ROUND(SUM(Total_Revenue), 2) AS Monthly_Revenue_INR,
    ROUND(SUM(Gross_Profit), 2) AS Monthly_Gross_Profit_INR,
    ROUND((SUM(Gross_Profit) * 100.0) / SUM(Total_Revenue), 2) AS Monthly_Margin_Pct
FROM sales_data
GROUP BY Year_Month
ORDER BY Year_Month ASC;

-- ----------------------------------------------------------------------
-- QUERY 5: Brand-Wise Profitability Summary
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 5
```sql
SELECT 
    Brand,
    COUNT(Sale_ID) AS Transaction_Count,
    SUM(Quantity) AS Units_Sold,
    ROUND(SUM(Total_Revenue), 2) AS Total_Revenue_INR,
    ROUND(SUM(Gross_Profit), 2) AS Total_Gross_Profit_INR,
    ROUND((SUM(Gross_Profit) * 100.0) / SUM(Total_Revenue), 2) AS Brand_Margin_Pct,
    ROUND(AVG(Discount), 2) AS Avg_Discount_Given_INR
FROM sales_data
GROUP BY Brand
ORDER BY Total_Revenue_INR DESC;

-- ----------------------------------------------------------------------
-- QUERY 6: Category-Wise Profitability
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 6
```sql
SELECT 
    Vehicle_Category,
    SUM(Quantity) AS Units_Sold,
    ROUND(SUM(Total_Revenue), 2) AS Total_Revenue_INR,
    ROUND(SUM(Gross_Profit), 2) AS Total_Gross_Profit_INR,
    ROUND((SUM(Gross_Profit) * 100.0) / SUM(Total_Revenue), 2) AS Category_Margin_Pct,
    ROUND(AVG(Selling_Price), 2) AS Avg_Selling_Price_INR
FROM sales_data
GROUP BY Vehicle_Category
ORDER BY Total_Gross_Profit_INR DESC;

-- ----------------------------------------------------------------------
-- QUERY 7: Total Inventory Valuation & Current Stock Units
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 7
```sql
SELECT 
    COUNT(Inventory_ID) AS Total_Units_In_Stock,
    ROUND(SUM(Stock_Value), 2) AS Total_Inventory_Valuation_INR,
    ROUND(AVG(Stock_Value), 2) AS Avg_Cost_Per_Unit_INR,
    ROUND(SUM(Annual_Holding_Cost), 2) AS Annual_Carrying_Cost_INR
FROM inventory_data;

-- ----------------------------------------------------------------------
-- QUERY 8: Slow-Moving Inventory Identification (>90 Days)
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 8
```sql
SELECT 
    Inventory_ID,
    Vehicle_ID,
    Brand,
    Model,
    Warehouse_Location,
    Days_In_Inventory,
    ROUND(Stock_Value, 2) AS Capital_Blocked_INR,
    ROUND(Holding_Cost_Incurred, 2) AS Holding_Cost_Incurred_INR
FROM inventory_data
WHERE Days_In_Inventory > 90
ORDER BY Days_In_Inventory DESC
LIMIT 15;

-- ----------------------------------------------------------------------
-- QUERY 9: Inventory Turnover by Vehicle Model
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 9
```sql
WITH Model_COGS AS (
    SELECT Model, CAST(SUM(Vehicle_Cost) AS FLOAT) AS Annual_COGS
    FROM sales_data
    WHERE Year = 2025
    GROUP BY Model
),
Model_Stock AS (
    SELECT Model, CAST(SUM(Stock_Value) AS FLOAT) AS Current_Stock_Val, COUNT(Inventory_ID) AS Units_In_Stock
    FROM inventory_data
    GROUP BY Model
)
SELECT 
    s.Model,
    s.Units_In_Stock,
    ROUND(s.Current_Stock_Val, 2) AS Current_Stock_Value_INR,
    ROUND(COALESCE(c.Annual_COGS, 0), 2) AS Annual_COGS_2025_INR,
    ROUND(COALESCE(c.Annual_COGS, 0) / s.Current_Stock_Val, 2) AS Inventory_Turnover_Ratio,
    ROUND((s.Current_Stock_Val / NULLIF(c.Annual_COGS, 0.0)) * 365.0, 1) AS Days_Sales_Inventory
FROM Model_Stock s
LEFT JOIN Model_COGS c ON s.Model = c.Model
ORDER BY Inventory_Turnover_Ratio DESC;

-- ----------------------------------------------------------------------
-- QUERY 10: Stock Aging Analysis by Bracket
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 10
```sql
SELECT 
    Aging_Bucket,
    COUNT(Inventory_ID) AS Vehicle_Count,
    ROUND(SUM(Stock_Value), 2) AS Total_Stock_Value_INR,
    ROUND((SUM(Stock_Value) * 100.0) / (SELECT SUM(Stock_Value) FROM inventory_data), 2) AS Stock_Share_Pct,
    ROUND(SUM(Annual_Holding_Cost), 2) AS Annual_Holding_Cost_INR
FROM inventory_data
GROUP BY Aging_Bucket
ORDER BY 
    CASE Aging_Bucket
        WHEN '0-30 Days (Fresh)' THEN 1
        WHEN '31-60 Days (Normal)' THEN 2
        WHEN '61-90 Days (Aging)' THEN 3
        WHEN '91-120 Days (Slow Moving)' THEN 4
        WHEN '120+ Days (Critical)' THEN 5
        ELSE 6
    END;

-- ----------------------------------------------------------------------
-- QUERY 11: Monthly Units Sold
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 11
```sql
SELECT 
    Year_Month,
    SUM(Quantity) AS Total_Units_Sold,
    COUNT(DISTINCT Customer_ID) AS Total_Customers_Served,
    ROUND(AVG(Quantity), 2) AS Avg_Units_Per_Transaction
FROM sales_data
GROUP BY Year_Month
ORDER BY Year_Month ASC;

-- ----------------------------------------------------------------------
-- QUERY 12: Average Selling Price (ASP) by Brand & Category
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 12
```sql
SELECT 
    Brand,
    Vehicle_Category,
    COUNT(Sale_ID) AS Sales_Count,
    ROUND(AVG(Selling_Price), 2) AS Avg_Selling_Price_INR,
    ROUND(MIN(Selling_Price), 2) AS Min_Price_INR,
    ROUND(MAX(Selling_Price), 2) AS Max_Price_INR
FROM sales_data
GROUP BY Brand, Vehicle_Category
ORDER BY Brand, Avg_Selling_Price_INR DESC;

-- ----------------------------------------------------------------------
-- QUERY 13: Average Discount by Brand
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 13
```sql
SELECT 
    Brand,
    SUM(Quantity) AS Total_Units,
    ROUND(AVG(Discount), 2) AS Avg_Discount_INR,
    ROUND(AVG(Discount_Pct), 2) AS Avg_Discount_Pct,
    ROUND(SUM(Discount), 2) AS Total_Discounts_Given_INR
FROM sales_data
GROUP BY Brand
ORDER BY Avg_Discount_Pct DESC;

-- ----------------------------------------------------------------------
-- QUERY 14: Accounts Receivable Aging Schedule
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 14
```sql
SELECT 
    AR_Aging_Bucket,
    COUNT(Invoice_ID) AS Open_Invoice_Count,
    ROUND(SUM(Outstanding_Amount), 2) AS Total_Receivables_INR,
    ROUND((SUM(Outstanding_Amount) * 100.0) / (SELECT SUM(Outstanding_Amount) FROM accounts_receivable WHERE Outstanding_Amount > 0), 2) AS Share_Pct
FROM accounts_receivable
WHERE Outstanding_Amount > 0
GROUP BY AR_Aging_Bucket
ORDER BY 
    CASE AR_Aging_Bucket
        WHEN 'Current (Not Due)' THEN 1
        WHEN '1-30 Days Overdue' THEN 2
        WHEN '31-60 Days Overdue' THEN 3
        WHEN '61-90 Days Overdue' THEN 4
        WHEN '90+ Days Overdue' THEN 5
        ELSE 6
    END;

-- ----------------------------------------------------------------------
-- QUERY 15: Accounts Payable Aging Schedule
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 15
```sql
SELECT 
    AP_Aging_Bucket,
    COUNT(Bill_ID) AS Open_Bill_Count,
    ROUND(SUM(Outstanding_Payable), 2) AS Total_Payables_INR,
    ROUND((SUM(Outstanding_Payable) * 100.0) / (SELECT SUM(Outstanding_Payable) FROM accounts_payable WHERE Outstanding_Payable > 0), 2) AS Share_Pct
FROM accounts_payable
WHERE Outstanding_Payable > 0
GROUP BY AP_Aging_Bucket
ORDER BY 
    CASE AP_Aging_Bucket
        WHEN 'Current (Not Due)' THEN 1
        WHEN '1-30 Days Overdue' THEN 2
        WHEN '31-60 Days Overdue' THEN 3
        WHEN '61-90 Days Overdue' THEN 4
        WHEN '90+ Days Overdue' THEN 5
        ELSE 6
    END;

-- ----------------------------------------------------------------------
-- QUERY 16: Top Outstanding Customer Payments
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 16
```sql
SELECT 
    Invoice_ID,
    Customer_ID,
    Invoice_Date,
    Due_Date,
    Days_Overdue,
    Payment_Status,
    ROUND(Invoice_Amount, 2) AS Invoice_Amount_INR,
    ROUND(Outstanding_Amount, 2) AS Outstanding_Amount_INR
FROM accounts_receivable
WHERE Outstanding_Amount > 0
ORDER BY Outstanding_Amount DESC
LIMIT 10;

-- ----------------------------------------------------------------------
-- QUERY 17: Outstanding Supplier Payments
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 17
```sql
SELECT 
    Bill_ID,
    Supplier_ID,
    Bill_Date,
    Due_Date,
    Days_Overdue,
    Payment_Status,
    ROUND(Bill_Amount, 2) AS Bill_Amount_INR,
    ROUND(Outstanding_Payable, 2) AS Outstanding_Payable_INR
FROM accounts_payable
WHERE Outstanding_Payable > 0
ORDER BY Outstanding_Payable DESC
LIMIT 10;

-- ----------------------------------------------------------------------
-- QUERY 18: Monthly Operating Expenses by Category
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 18
```sql
SELECT 
    Expense_Category,
    COUNT(Expense_ID) AS Expense_Entries,
    ROUND(SUM(Amount), 2) AS Total_Cost_INR,
    ROUND(AVG(Amount), 2) AS Avg_Monthly_Cost_INR,
    ROUND((SUM(Amount) * 100.0) / (SELECT SUM(Amount) FROM operating_expenses), 2) AS Expense_Share_Pct
FROM operating_expenses
GROUP BY Expense_Category
ORDER BY Total_Cost_INR DESC;

-- ----------------------------------------------------------------------
-- QUERY 19: Working Capital Calculation
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 19
```sql
WITH Balances AS (
    SELECT 
        285000000.0 AS Cash_Bank,
        (SELECT SUM(Outstanding_Amount) FROM accounts_receivable WHERE Outstanding_Amount > 0) AS Open_AR,
        (SELECT SUM(Stock_Value) FROM inventory_data) AS Stock_Inventory,
        42500000.0 AS Prepaids_Advances,
        (SELECT SUM(Outstanding_Payable) FROM accounts_payable WHERE Outstanding_Payable > 0) AS Open_AP,
        (SELECT SUM(Stock_Value) * 0.45 FROM inventory_data) AS Bank_Floorplan_OD,
        38500000.0 AS Accrued_Expenses_Taxes
)
SELECT 
    ROUND(Cash_Bank + Open_AR + Stock_Inventory + Prepaids_Advances, 2) AS Total_Current_Assets_INR,
    ROUND(Open_AP + Bank_Floorplan_OD + Accrued_Expenses_Taxes, 2) AS Total_Current_Liabilities_INR,
    ROUND((Cash_Bank + Open_AR + Stock_Inventory + Prepaids_Advances) - (Open_AP + Bank_Floorplan_OD + Accrued_Expenses_Taxes), 2) AS Net_Working_Capital_INR
FROM Balances;

-- ----------------------------------------------------------------------
-- QUERY 20: Current Ratio
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 20
```sql
WITH Balances AS (
    SELECT 
        (285000000.0 + 
         (SELECT SUM(Outstanding_Amount) FROM accounts_receivable WHERE Outstanding_Amount > 0) + 
         (SELECT SUM(Stock_Value) FROM inventory_data) + 
         42500000.0) AS Current_Assets,
        ((SELECT SUM(Outstanding_Payable) FROM accounts_payable WHERE Outstanding_Payable > 0) + 
         (SELECT SUM(Stock_Value) * 0.45 FROM inventory_data) + 
         38500000.0) AS Current_Liabilities
)
SELECT 
    ROUND(Current_Assets, 2) AS Current_Assets_INR,
    ROUND(Current_Liabilities, 2) AS Current_Liabilities_INR,
    ROUND(Current_Assets / Current_Liabilities, 3) AS Current_Ratio
FROM Balances;

-- ----------------------------------------------------------------------
-- QUERY 21: Quick Ratio
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 21
```sql
WITH Balances AS (
    SELECT 
        (285000000.0 + 
         (SELECT SUM(Outstanding_Amount) FROM accounts_receivable WHERE Outstanding_Amount > 0) + 
         42500000.0) AS Quick_Assets,
        ((SELECT SUM(Outstanding_Payable) FROM accounts_payable WHERE Outstanding_Payable > 0) + 
         (SELECT SUM(Stock_Value) * 0.45 FROM inventory_data) + 
         38500000.0) AS Current_Liabilities
)
SELECT 
    ROUND(Quick_Assets, 2) AS Quick_Assets_INR,
    ROUND(Current_Liabilities, 2) AS Current_Liabilities_INR,
    ROUND(Quick_Assets / Current_Liabilities, 3) AS Quick_Ratio
FROM Balances;

-- ----------------------------------------------------------------------
-- QUERY 22: Cash Conversion Cycle
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 22
```sql
WITH WorkingCapitalBase AS (
    SELECT 
        (SELECT SUM(Vehicle_Cost) FROM sales_data WHERE Year = 2025) AS Annual_COGS,
        (SELECT SUM(Total_Revenue) FROM sales_data WHERE Year = 2025 AND (Payment_Mode IN ('Auto Loan / Bank Finance', 'Bank Transfer / NEFT') OR Sales_Channel = 'Corporate Sales')) AS Annual_Credit_Sales,
        (SELECT SUM(Bill_Amount) FROM accounts_payable WHERE strftime('%Y', Bill_Date) = '2025') AS Annual_Credit_Purchases,
        (SELECT SUM(Stock_Value) * 0.975 FROM inventory_data) AS Avg_Inventory,
        (SELECT SUM(Outstanding_Amount) * 0.96 FROM accounts_receivable WHERE Outstanding_Amount > 0) AS Avg_AR,
        (SELECT SUM(Outstanding_Payable) * 0.97 FROM accounts_payable WHERE Outstanding_Payable > 0) AS Avg_AP
)
SELECT 
    ROUND((Avg_Inventory / Annual_COGS) * 365.0, 1) AS Days_Inventory_Outstanding_DIO,
    ROUND((Avg_AR / Annual_Credit_Sales) * 365.0, 1) AS Days_Sales_Outstanding_DSO,
    ROUND((Avg_AP / Annual_Credit_Purchases) * 365.0, 1) AS Days_Payable_Outstanding_DPO,
    ROUND(((Avg_Inventory / Annual_COGS) * 365.0) + ((Avg_AR / Annual_Credit_Sales) * 365.0) - ((Avg_AP / Annual_Credit_Purchases) * 365.0), 1) AS Cash_Conversion_Cycle_Days
FROM WorkingCapitalBase;

-- ----------------------------------------------------------------------
-- QUERY 23: Budget versus Actual Revenue
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 23
```sql
SELECT 
    Month,
    ROUND(Budget_Revenue, 2) AS Budget_Revenue_INR,
    ROUND(Actual_Revenue, 2) AS Actual_Revenue_INR,
    ROUND(Revenue_Variance, 2) AS Revenue_Variance_INR,
    ROUND(Revenue_Variance_Pct, 2) AS Revenue_Variance_Pct,
    Revenue_Status,
    ROUND(Revenue_Achievement_Pct, 1) AS Achievement_Pct
FROM monthly_budget
ORDER BY Month ASC;

-- ----------------------------------------------------------------------
-- QUERY 24: Budget versus Actual Expenses
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 24
```sql
SELECT 
    Month,
    ROUND(Budget_Expenses, 2) AS Budget_Expenses_INR,
    ROUND(Actual_Expenses, 2) AS Actual_Expenses_INR,
    ROUND(Expense_Variance, 2) AS Expense_Variance_INR,
    ROUND(Expense_Variance_Pct, 2) AS Expense_Variance_Pct,
    Expense_Status
FROM monthly_budget
ORDER BY Month ASC;

-- ----------------------------------------------------------------------
-- QUERY 25: Best-Performing Sales Consultants
-- ----------------------------------------------------------------------
```

**Result Output:**

### Query 25
```sql
SELECT 
    Salesperson_ID,
    COUNT(Sale_ID) AS Total_Deals_Closed,
    SUM(Quantity) AS Total_Vehicles_Sold,
    ROUND(SUM(Total_Revenue), 2) AS Total_Revenue_Generated_INR,
    ROUND(SUM(Gross_Profit), 2) AS Gross_Profit_Contributed_INR,
    ROUND((SUM(Gross_Profit) * 100.0) / SUM(Total_Revenue), 2) AS Realized_Margin_Pct,
    ROUND(AVG(Discount), 2) AS Avg_Discount_Per_Vehicle_INR
FROM sales_data
GROUP BY Salesperson_ID
ORDER BY Gross_Profit_Contributed_INR DESC;
```

**Result Output:**
