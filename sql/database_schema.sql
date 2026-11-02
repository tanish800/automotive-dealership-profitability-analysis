-- =============================================================================
-- SQL SCHEMA: database_schema.sql
-- PROJECT: Automotive Dealership Profitability & Working Capital Analysis
-- DATABASE: SQLite 3 (dealership.db)
-- DATASET: Genuine CarDekho Used Vehicle Listing Dataset
-- =============================================================================

DROP TABLE IF EXISTS vehicles;

CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    year INTEGER NOT NULL,
    selling_price REAL NOT NULL,
    km_driven REAL NOT NULL,
    fuel TEXT NOT NULL,
    seller_type TEXT NOT NULL,
    transmission TEXT NOT NULL,
    owner TEXT NOT NULL,
    mileage TEXT,
    engine TEXT,
    max_power TEXT,
    torque TEXT,
    seats REAL,
    Vehicle_Brand TEXT NOT NULL,
    Vehicle_Model TEXT NOT NULL,
    Mileage_kmpl REAL,
    Engine_cc REAL,
    Max_Power_bhp REAL,
    Vehicle_Age INTEGER NOT NULL,
    Vehicle_Age_Group TEXT NOT NULL,
    Price_Category TEXT NOT NULL,
    Kilometres_Category TEXT NOT NULL,
    Mileage_Category TEXT NOT NULL,
    Ownership_Category TEXT NOT NULL,
    Fuel_Category TEXT NOT NULL,
    Transmission_Category TEXT NOT NULL,
    Seller_Category TEXT NOT NULL,
    Is_Price_Outlier INTEGER DEFAULT 0,
    Is_KM_Outlier INTEGER DEFAULT 0
);

-- Optimize query performance across core analytical dimensions
CREATE INDEX idx_vehicle_brand ON vehicles(Vehicle_Brand);
CREATE INDEX idx_vehicle_model ON vehicles(Vehicle_Model);
CREATE INDEX idx_selling_price ON vehicles(selling_price);
CREATE INDEX idx_vehicle_age ON vehicles(Vehicle_Age);
CREATE INDEX idx_fuel ON vehicles(Fuel_Category);
CREATE INDEX idx_transmission ON vehicles(Transmission_Category);
CREATE INDEX idx_seller ON vehicles(Seller_Category);
CREATE INDEX idx_price_cat ON vehicles(Price_Category);
