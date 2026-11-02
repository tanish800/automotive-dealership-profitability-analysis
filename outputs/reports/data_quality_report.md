# DATA QUALITY AND PREPROCESSING AUDIT REPORT

**Baseline Analysis Year:** 2026 | **Generated:** 2026-11-02 18:06

## 1. Executive Data Audit Summary

- **Raw Record Count:** 8,128
- **Duplicate Listings Identified & Deduplicated:** 1,202 (14.8%)
- **Final Cleaned Unique Listings:** 6,926
- **Analyzed Automotive Brands:** 32
- **Analyzed Vehicle Models:** 629

## 2. Statistical Distribution of Cleaned Listing Population

| Dimension | Minimum | 25th Percentile | Median | Mean | 75th Percentile | Maximum |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Selling Price (₹)** | ₹29,999 | ₹250,000 | ₹400,000 | ₹517,271 | ₹633,500 | ₹10,000,000 |
| **Kilometres Driven** | 1 | 40,000 | 70,000 | 73,996 | 100,000 | 2,360,457 |
| **Vehicle Age (Years)** | 6 | 9 | 12 | 12.6 | 15 | 43 |

## 3. Outlier Audit (IQR Fence Method: 1.5 * IQR)

- **Selling Price Outliers:** 328 listings (> ₹1,208,750 luxury exotic outliers)
- **KM Driven Outliers:** 167 listings (> 190,000 commercial/fleet mileage outliers)
- **Vehicle Age Outliers:** 77 listings (> 24 years vintage outliers)

## 4. Derived Categorical Column Architecture

- `Vehicle_Brand`: Standardized OEM manufacturer (e.g. Maruti, Hyundai, Land Rover)
- `Vehicle_Model`: Extracted model line excluding variant trim suffixes
- `Vehicle_Age`: Current year (2026) minus vehicle manufacturing year
- `Vehicle_Age_Group`: Under 7 Yrs (Recent), 7-10 Yrs (Mid-Age), 11-15 Yrs (Mature), Over 15 Yrs (Aged)
- `Price_Category`: Budget (<₹3L), Mid-Range (₹3L-₹6L), Upper Mid-Range (₹6L-₹10L), Premium (₹10L-₹20L), Luxury (>₹20L)
- `Kilometres_Category`: Low (<30k), Moderate (30k-60k), High (60k-100k), Very High (>100k)
- `Mileage_Category`: Low (<15 kmpl), Moderate (15-20 kmpl), High (>20 kmpl), Not Specified
- `Ownership_Category`, `Fuel_Category`, `Transmission_Category`, `Seller_Category`
