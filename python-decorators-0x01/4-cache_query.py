import sqlite3
import functools

# Cache dictionary to store query results
query_cache = {}

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

def cache_query(func):
    """Decorator to cache query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Fetching from cache...")
            return query_cache[query]  # Return cached result

        # Call the original function and cache the result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result  # Store result in cache
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from the database and cache the result."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Example usage: Fetch users with caching
if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)