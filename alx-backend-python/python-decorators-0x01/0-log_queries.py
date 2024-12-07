import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """Decorator to log SQL queries with a timestamp."""
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing query: {query}")  # Log the query with timestamp
        return func(query, *args, **kwargs)  # Call the original function
    return wrapper

@log_queries
def fetch_all_users(query):
    """Fetch all users from the database based on the provided SQL query."""
    conn = sqlite3.connect('users.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor
    cursor.execute(query)  # Execute the query
    results = cursor.fetchall()  # Fetch all results
    conn.close()  # Close the connection
    return results

# Example usage: fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)