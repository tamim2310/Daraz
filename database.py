import sqlite3

def init_db():
    conn = sqlite3.connect("tracker.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tracking (
            user_id INTEGER,
            url TEXT,
            target_price REAL,
            PRIMARY KEY (user_id, url)
        )
    """)
    conn.commit()
    conn.close()

def add_tracking(user_id, url, target_price):
    conn = sqlite3.connect("tracker.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO tracking (user_id, url, target_price) VALUES (?, ?, ?)",
              (user_id, url, target_price))
    conn.commit()
    conn.close()

def get_all_tracking():
    conn = sqlite3.connect("tracker.db")
    c = conn.cursor()
    c.execute("SELECT user_id, url, target_price FROM tracking")
    rows = c.fetchall()
    conn.close()
    return rows
