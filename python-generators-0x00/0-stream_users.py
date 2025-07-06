seed = __import__('seed')

def stream_users():
    """Generator that streams rows from user_data table one at a time."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()