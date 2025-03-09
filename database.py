import sqlite3
from datetime import datetime

DB_NAME = 'opportunities.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        link TEXT NOT NULL,
        domain TEXT,
        opportunity_type TEXT,
        fully_funded INTEGER,
        date TEXT
    )''')
    conn.commit()
    conn.close()

def add_opportunity(title, description, link, domain, opportunity_type, fully_funded, date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO opportunities (title, description, link, domain, opportunity_type, fully_funded, date)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (title, description, link, domain, opportunity_type, fully_funded, date))
    conn.commit()
    conn.close()

def get_opportunities():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT title, description, link, domain, opportunity_type, fully_funded, date FROM opportunities')
    rows = c.fetchall()
    conn.close()
    return [{'title': r[0], 'description': r[1], 'link': r[2], 'domain': r[3],
             'opportunity_type': r[4], 'fully_funded': r[5], 'date': r[6]} for r in rows]