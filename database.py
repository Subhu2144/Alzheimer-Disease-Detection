import sqlite3
import os
from datetime import datetime
from config import DB_PATH


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            image_name TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_prediction(username, image_name, prediction, confidence):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (username, image_name, prediction, confidence, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        image_name,
        prediction,
        confidence,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_predictions(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT image_name, prediction, confidence, created_at
        FROM predictions
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    records = cursor.fetchall()
    conn.close()

    return records