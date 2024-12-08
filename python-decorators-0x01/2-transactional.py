import sqlite3
import functools

def with_db_connection(func):
    """Decorator to handle database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection to the original function
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed
            conn.close()
    return wrapper

def transactional(func):
    """Decorator to manage database transactions."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the original function
            result = func(conn, *args, **kwargs)
            # Commit the transaction if no exceptions were raised
            conn.commit()
            return result
        except Exception as e:
            # Rollback the transaction in case of error
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise  # Re-raise the exception for further handling
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Update user's email with automatic transaction handling."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Example usage: Update email for user with ID 1
if __name__ == "__main__":
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        print("Email updated successfully.")
    except Exception:
        print("Failed to update email.")