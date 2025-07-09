import sqlite3
import csv

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age TEXT,
        UNIQUE(name, email)
    )
"""
)

try:
    with open("users_data.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                cursor.execute(
                    """
                    INSERT INTO users (name, email, age)
                    values (?, ?, ?)
                """,
                    (row["name"], row["email"], row["age"]),
                )
            except sqlite3.IntegrityError:
                print(f"(Skiping duplicate user, {row["name"]})")


except FileNotFoundError:
    print("File, users_data.csv not found")

conn.commit()
conn.close()