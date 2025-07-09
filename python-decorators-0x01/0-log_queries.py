import functools
import logging
import sqlite3

def log_queries(func):
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        if 'query' in kwargs:
            logging.info(f"SQL Query: {kwargs['query']}")
        return func(*args, **kwargs)
    return wrapper_log_queries

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
    