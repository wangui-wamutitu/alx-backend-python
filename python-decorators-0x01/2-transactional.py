import functools
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

def transactional(func):
    @functools.wraps(func)
    def wrapper_transactional(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print(f"Transaction successful: {result}")
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back: {e}")
    return wrapper_transactional

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    if cursor.rowcount == 0:
        raise ValueError(f"No user found with ID {user_id}.")
    return f"Updated user {user_id} with email {new_email}"

# Update user's email with automatic transaction handling 
update_user_email(user_id='904330', new_email='Crawford_Cartwright@hotmail.com')