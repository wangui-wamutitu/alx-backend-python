import functools
import time
import sqlite3

query_cache = {} #in-memory cache

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        conn = None
        try: 
            conn = sqlite3.connect("app.db")  
            return func(conn, *args, **kwargs)
        finally:
            if conn:
                conn.close()        
    return wrapper_with_db_connection

def cache_query(func):
    @functools.wraps(func)
    def wrapper_cache_query(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query is None:
            raise ValueError("Missing SQL query")

        if query in query_cache:
            print("Returning cached result for query")
            return query_cache[query]

        print("Querying DB and caching result")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper_cache_query

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
    