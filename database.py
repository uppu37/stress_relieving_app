import sqlite3
from datetime import datetime

def create_table():
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS journal(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            mood TEXT,
            score REAL,
            entry TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_entry(mood, score, text):
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO journal (date, mood, score, entry) VALUES (?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mood, score, text)
    )
    conn.commit()
    conn.close()

def get_entries():
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM journal ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data