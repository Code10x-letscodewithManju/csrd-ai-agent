import sqlite3
import os

DB_PATH = "data/outputs/csrd_data.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open("src/db/schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.close()

def insert_row(row: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    sql = """
    INSERT OR REPLACE INTO extracted_metrics 
    (company, report_year, indicator_name, value, unit, confidence, source_page, source_section, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cur.execute(sql, (
        row["company"],
        row["report_year"],
        row["indicator_name"],
        row["value"],
        row["unit"],
        row["confidence"],
        row["source_page"],
        row["source_section"],
        row["notes"]
    ))
    
    conn.commit()
    conn.close()