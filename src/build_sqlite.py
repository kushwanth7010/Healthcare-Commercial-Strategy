"""Build a local SQLite warehouse and export sample SQL results."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def build():
    output=ROOT/"outputs"
    output.mkdir(exist_ok=True)
    db=output/"healthcare_strategy.db"
    if db.exists(): db.unlink()
    with sqlite3.connect(db) as con:
        con.execute("PRAGMA foreign_keys=ON")
        con.executescript((ROOT/"sql"/"01_schema.sql").read_text())
        for table,filename in [
            ("products","products.csv"),("physicians","physicians.csv"),
            ("commercial_sales","commercial_sales.csv"),
            ("synthetic_therapy_episodes","synthetic_therapy_episodes.csv")]:
            data=pd.read_csv(ROOT/"data"/filename)
            data.to_sql(table,con,if_exists="append",index=False)
        # Export a reproducible SQL output with ranking.
        q="""WITH totals AS (SELECT region,product_id,SUM(revenue_inr-cogs_inr) gross_profit_inr
                FROM commercial_sales GROUP BY region,product_id)
                SELECT region,product_id,gross_profit_inr,
                DENSE_RANK() OVER (PARTITION BY region ORDER BY gross_profit_inr DESC) profit_rank
                FROM totals ORDER BY region, profit_rank"""
        ranked=pd.read_sql_query(q,con)
        ranked.to_csv(output/"sql_region_product_profit_ranks.csv",index=False)
        count=con.execute("SELECT COUNT(*) FROM commercial_sales").fetchone()[0]
    print(f"SQLITE built at {db}; validated {count} sales records")

if __name__=="__main__":build()
