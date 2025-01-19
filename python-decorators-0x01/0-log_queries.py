import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """
    Decorator to log SQL queries before executing them
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if the first argument is a query
        if args and isinstance(args[0], str):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Executing query: {args[0]}")
        
        # Execute the original function
        return func(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
users = fetch_all_users(query="SELECT * FROM users")