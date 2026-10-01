"""Run all six educational SQL queries against the generated SQLite database."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def run_all():
    query_text=(ROOT/"sql"/"02_analysis_queries.sql").read_text(encoding="utf-8")
    statements=[q.strip() for q in query_text.split(";") if q.strip()]
    db=ROOT/"outputs"/"healthcare_strategy.db"
    if not db.exists():
        raise FileNotFoundError("Run python -m src.build_sqlite first")
    with sqlite3.connect(db) as con:
        for i,statement in enumerate(statements,1):
            frame=pd.read_sql_query(statement,con)
            dest=ROOT/"outputs"/f"sql_query_{i}_results.csv"
            frame.to_csv(dest,index=False)
            print(f"SQL query {i}: {len(frame)} rows -> {dest.name}")
    return len(statements)

if __name__=="__main__":run_all()
