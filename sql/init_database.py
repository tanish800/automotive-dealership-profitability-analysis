"""
AutoFinance Analytics - Database Initialization & Analytical Query Execution Engine
Module: sql/init_database.py

Performs:
1. Creates SQLite database at sql/autofinance.db.
2. Executes DDL schema from sql/schema.sql.
3. Loads all cleaned CSV datasets into relational tables.
4. Executes and validates all 25 business analytical queries.
5. Exports query execution outputs to sql/query_results.txt and sql/query_results.md.
"""

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "sql", "autofinance.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "sql", "schema.sql")
QUERIES_PATH = os.path.join(BASE_DIR, "sql", "business_analysis.sql")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
RESULTS_PATH = os.path.join(BASE_DIR, "sql", "query_results.txt")
MD_RESULTS_PATH = os.path.join(BASE_DIR, "sql", "query_results.md")


def setup_and_run_database():
    print("=" * 70)
    print("AutoFinance Analytics: Database Initialization & SQL Query Engine")
    print("=" * 70)
    
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"Removed existing database for fresh build: {DB_PATH}")
        except Exception:
            pass
            
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("1. Creating database tables and indexes from schema.sql...")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    print("   -> Schema DDL executed successfully.")
    
    print("2. Ingesting cleaned datasets into SQLite relational tables...")
    table_files = [
        ("vehicle_master", "vehicle_master_clean.csv"),
        ("sales_data", "vehicle_sales_clean.csv"),
        ("inventory_data", "inventory_data_clean.csv"),
        ("operating_expenses", "operating_expenses_clean.csv"),
        ("accounts_receivable", "accounts_receivable_clean.csv"),
        ("accounts_payable", "accounts_payable_clean.csv"),
        ("monthly_budget", "monthly_budget_clean.csv"),
    ]
    
    for table_name, csv_file in table_files:
        csv_path = os.path.join(PROCESSED_DIR, csv_file)
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists="append", index=False)
        count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"   -> Loaded {table_name}: {count:,} records")
        
    conn.commit()
    
    print("\n3. Executing all 25 Business Analytical SQL Queries...")
    with open(QUERIES_PATH, "r", encoding="utf-8") as f:
        full_sql = f.read()
        
    raw_sections = full_sql.split("-- Query_")
    output_lines = []
    md_output_lines = ["# AutoFinance Analytics: SQL Business Query Execution Results\n"]
    output_lines.append("=" * 75)
    output_lines.append("AUTOFINANCE ANALYTICS: 25 CORE BUSINESS ANALYTICAL SQL QUERY OUTPUTS")
    output_lines.append("=" * 75 + "\n")
    
    executed_count = 0
    for section in raw_sections[1:]:
        if not section.strip():
            continue
        lines = section.strip().split("\n")
        query_num = lines[0].strip()
        sql_text = "\n".join(lines[1:]).strip()
        if not sql_text:
            continue
            
        executed_count += 1
        print(f"   Executing Query {query_num}...")
        
        try:
            res_df = pd.read_sql_query(sql_text, conn)
            output_lines.append(f"--- [QUERY {query_num}] ---")
            output_lines.append(res_df.to_string(index=False))
            output_lines.append("-" * 75 + "\n")
            
            md_output_lines.append(f"### Query {query_num}")
            md_output_lines.append("```sql\n" + sql_text + "\n```")
            md_output_lines.append("\n**Result Output:**\n")
            md_output_lines.append(res_df.to_markdown(index=False) if hasattr(res_df, "to_markdown") else res_df.to_string(index=False))
            md_output_lines.append("\n---\n")
            
            if executed_count in [1, 2, 8, 10, 19, 20, 22]:
                print(f"   Sample Output for Query {query_num}:")
                print("   " + res_df.head(2).to_string(index=False).replace("\n", "\n   "))
                print()
        except Exception as e:
            print(f"   ERROR in Query {query_num}: {e}")
            output_lines.append(f"--- [QUERY {query_num} ERROR]: {e} ---\n")
            
    with open(RESULTS_PATH, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(output_lines))
        
    with open(MD_RESULTS_PATH, "w", encoding="utf-8") as md_f:
        md_f.write("\n".join(md_output_lines))
        
    conn.close()
    print(f"\nSuccessfully executed all {executed_count} queries!")
    print(f"Query results saved to: {RESULTS_PATH} and {MD_RESULTS_PATH}")
    print(f"SQLite Database: {DB_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    setup_and_run_database()
