seed = __import__('seed')

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of rows from user_data table.
    Each batch is a list of rows.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes user_data in batches and yields users with age > 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        filtered = [row for row in batch if float(row[3]) > 25]  # loop 2 (inside list comp)
        for user in filtered:  # loop 3
            yield user
