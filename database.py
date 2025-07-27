import sqlite3
import hashlib

def create_connection():
    return sqlite3.connect("user_data.db")

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usb_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_time TEXT,
        event_type TEXT,
        description TEXT
    )""")
    conn.commit()
    conn.close()

def register_user(username, email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_user(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user