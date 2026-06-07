import sqlite3

def connect_db():
    conn = sqlite3.connect("database/smart_hire.db")
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
    INSERT INTO candidates
    (name, email, phone, skills, experience, score)
    VALUES (?, ?, ?, ?, ?, ?)
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
