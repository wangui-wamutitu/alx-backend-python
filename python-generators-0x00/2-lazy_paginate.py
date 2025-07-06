seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch one page of user data from offset."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def lazy_paginate(page_size):
    """Generator that lazily paginates user data one page at a time."""
    offset = 0
    while True:  
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

