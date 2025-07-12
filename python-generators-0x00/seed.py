import mysql.connector
import uuid
import csv

def connect_db():
    """Connects to MySQL server (without database)."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Creates ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists.")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to ALX_prodev database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="ALX_prodev"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Creates user_data table if it doesn't exist."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX(user_id)
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Table user_data created or already exists.")
    cursor.close()

def insert_data(connection, csv_file):
    """Inserts users from CSV if not already in the database (by email)."""
    cursor = connection.cursor()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name']
            email = row['email']
            age = row['age']

            # Check if user already exists by email
            cursor.execute("SELECT user_id FROM user_data WHERE email = %s", (email,))
            if cursor.fetchone():
                print(f"User with email {email} already exists. Skipping...")
                continue

            # Insert new user
            user_id = str(uuid.uuid4())
            insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, name, email, age))
            print(f"Inserted: {name}, {email}, {age}")

    connection.commit()
    cursor.close()
