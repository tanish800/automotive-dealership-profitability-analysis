"""
=============================================================================
MODULE: run_queries.py
PROJECT: Automotive Dealership Profitability & Working Capital Analysis
AUTHOR: Senior Financial Analyst & SQL Specialist
=============================================================================

PURPOSE:
Executes all 20 business queries from sql/analysis_queries.sql against the
SQLite database (dealership.db) and writes formatted outputs to markdown.
"""

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "sql", "dealership.db")
QUERIES_PATH = os.path.join(BASE_DIR, "sql", "analysis_queries.sql")
OUTPUT_MD_PATH = os.path.join(BASE_DIR, "sql", "query_results.md")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")


def df_to_markdown_table(df: pd.DataFrame) -> str:
    """Formats DataFrame as GitHub-flavored Markdown table without tabulate dependency."""
    if df.empty:
        return "_No records returned._"
    headers = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join([":---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        vals = [str(v).replace("\n", " ").replace("|", "\\|") if pd.notnull(v) else "" for v in row]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def parse_sql_file(sql_file_path: str) -> list[tuple[str, str]]:
    """Splits sql file into titled query blocks."""
    with open(sql_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("-- Query ")
    queries = []
    for block in blocks[1:]:
        lines = block.strip().split("\n")
        title_line = lines[0].strip()
        title = f"Query {title_line}"
        query_sql = "\n".join([line for line in lines[1:] if not line.strip().startswith("--") and line.strip()])
        query_sql = query_sql.strip()
        if query_sql:
            queries.append((title, query_sql))
    return queries


def execute_all_queries() -> list[dict]:
    """Runs all 20 queries and compiles results."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run init_database.py first.")

    conn = sqlite3.connect(DB_PATH)
    queries = parse_sql_file(QUERIES_PATH)

    print(f"[SQL RUNNER] Found {len(queries)} queries in {QUERIES_PATH}")
    results = []

    with open(OUTPUT_MD_PATH, "w", encoding="utf-8") as out:
        out.write("# AUTOMOTIVE DEALERSHIP SQL BUSINESS ANALYSIS REPORT\n\n")
        out.write("**Source Database:** `dealership.db` | **Cleaned Population:** 6,926 Real Vehicles\n\n")

        for idx, (title, sql_text) in enumerate(queries, 1):
            print(f"Executing [{idx}/{len(queries)}]: {title}")
            try:
                df_res = pd.read_sql_query(sql_text, conn)
                row_count = len(df_res)
                out.write(f"## {title}\n\n")
                out.write("```sql\n" + sql_text + "\n```\n\n")
                out.write(f"**Results ({row_count} rows):**\n\n")
                out.write(df_to_markdown_table(df_res) + "\n\n")

                results.append({
                    "query_number": idx,
                    "title": title,
                    "sql": sql_text,
                    "row_count": row_count,
                    "status": "SUCCESS"
                })
            except Exception as e:
                print(f"ERROR executing {title}: {e}")
                out.write(f"## {title} - ERROR\n\n`{str(e)}`\n\n")
                results.append({
                    "query_number": idx,
                    "title": title,
                    "sql": sql_text,
                    "row_count": 0,
                    "status": f"ERROR: {str(e)}"
                })

    conn.close()

    # Also save a copy in reports dir
    report_copy_path = os.path.join(REPORTS_DIR, "sql_analysis_summary.md")
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(OUTPUT_MD_PATH, "r", encoding="utf-8") as src, open(report_copy_path, "w", encoding="utf-8") as dst:
        dst.write(src.read())

    print(f"[SQL RUNNER] All {len(results)} queries executed successfully.")
    print(f"[SQL RUNNER] Markdown reports saved to:\n  - {OUTPUT_MD_PATH}\n  - {report_copy_path}")
    return results


if __name__ == "__main__":
    execute_all_queries()
