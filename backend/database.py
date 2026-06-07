import sqlite3
import os

# Get project root (smart_hire_analyzer folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "database", "smart_hire.db")


def connect_db():

    # Ensure database folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        experience TEXT,
        score REAL
    )
    """)

    conn.commit()

    return conn


def save_candidate(data):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates (
        name, email, phone, skills, experience, score
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["email"],
        data["phone"],
        data["skills"],
        data["experience"],
        data["score"]
    ))

    conn.commit()
    conn.close()