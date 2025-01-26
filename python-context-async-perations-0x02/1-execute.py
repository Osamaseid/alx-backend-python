import sqlite3

class ExecuteQuery:
    def __init__(self, database, query, params=None):
        self.database = database
        self.query = query
        self.params = params if params is not None else []
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Establish the database connection
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        return self  # Return the context manager itself

    def execute(self):
        # Execute the query with parameters
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()  # Fetch all results from the query

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Example usage of the ExecuteQuery context manager
if __name__ == "__main__":
    database = 'example.db'  # Replace with your database file

    # Create a sample database and users table for demonstration
    with sqlite3.connect(database) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
        conn.execute('INSERT INTO users (name, age) VALUES ("Alice", 30), ("Bob", 22), ("Carol", 28)')
        conn.commit()

    # Using the custom context manager to execute a query
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(database, query, params) as executor:
        results = executor.execute()  # Execute the query and get results
        for row in results:
            print(row)  # Print each row from the results