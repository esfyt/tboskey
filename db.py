import sqlite3

def init_db():
    conn = sqlite3.connect('license.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            key TEXT UNIQUE,
            used INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def store_key(email, key):
    conn = sqlite3.connect('license.db')
    c = conn.cursor()
    c.execute("INSERT INTO licenses (email, key) VALUES (?, ?)", (email, key))
    conn.commit()
    conn.close()

def check_key(key):
    conn = sqlite3.connect('license.db')
    c = conn.cursor()
    c.execute("SELECT used FROM licenses WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row

def mark_key_used(key):
    conn = sqlite3.connect('license.db')
    c = conn.cursor()
    c.execute("UPDATE licenses SET used=1 WHERE key=?", (key,))
    conn.commit()
    conn.close()
def store_user(email, pwd): ...
def verify_user(email, pwd): ...
def get_or_create_key(user_id):
    # Check existing, else generate new key via generate_activation_key()
    ...
