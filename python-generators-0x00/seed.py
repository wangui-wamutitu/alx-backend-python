seed = __import__('seed')
import csv

def read_csv(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        return [(row['name'], row['email'], row['age']) for row in reader]

# Step 1: Connect to MySQL server (no DB yet)
connection = seed.connect_db()

if connection:
    seed.create_database(connection)
    connection.close()
    print("✅ Connection successful")

    # Step 2: Connect to ALX_prodev DB
    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)

        # Step 3: Read CSV and insert data
        data = read_csv('user_data.csv')
        seed.insert_data(connection, data)

        # Step 4: Check if database exists
        cursor = connection.cursor()
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("✅ Database ALX_prodev is present")

        # Step 5: Preview inserted data
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print("📝 Sample rows:", rows)

        cursor.close()
        connection.close()