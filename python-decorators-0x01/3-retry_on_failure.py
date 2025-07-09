import functools
import time
import sqlite3


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

def retry_on_failure(retries, delay):
    def decorator(func):
        @functools.wraps(func)
        def wrapper_retry_on_failure(conn, *args, **kwargs):
            for attempt in range(retries):
                try:
                    result = func(conn, *args, **kwargs)
                    return result
                except sqlite3.OperationalError as e:
                    if "database is locked" in str(e).lower():
                        print(f"Attempt {attempt + 1}: DB is locked. Retrying...")
                        time.sleep(delay * (2 ** attempt)) 
                    else:
                        print(f"Non-transient error: {e}")
                        raise
            raise RuntimeError(f"Max attempts to communicate to the db reached. Operation failed")    
        return wrapper_retry_on_failure
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
    