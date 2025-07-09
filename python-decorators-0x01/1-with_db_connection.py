import functools
import sqlite3

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        conn = None
        try: 
            # connecting to the db
            conn = sqlite3.connect("app.db")
            return func(conn, *args, **kwargs)
        finally:
            # save changes and close connection if it is open
            if conn:
                conn.close()        

    return wrapper_with_db_connection

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 


# Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id=11)
print(user)