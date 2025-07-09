import sqlite3
import csv
import time

# connecting to the db
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# creates users table
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

# load data from users_data.csv
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

# Lock the database exclusively , tests retries
# cursor.execute("BEGIN EXCLUSIVE TRANSACTION")
# print("🔒 DB locked for 20 seconds")
# time.sleep(20)  

# save changes and close connection
conn.commit()
conn.close()
