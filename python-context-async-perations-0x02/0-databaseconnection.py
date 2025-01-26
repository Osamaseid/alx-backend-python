import sqlite3

class DatabaseConnection:
    def __init__(self, database):
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Establish the database connection
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        return self.cursor  # Return the cursor to perform queries

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Example usage of the DatabaseConnection context manager
if __name__ == "__main__":
    database = 'example.db'  # Replace with your database file

    # Create a sample database and users table for demonstration
    with sqlite3.connect(database) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
        conn.execute('INSERT INTO users (name) VALUES ("Alice"), ("Bob"), ("Carol")')
        conn.commit()

    # Using the custom context manager to fetch data
    with DatabaseConnection(database) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()  # Fetch all results from the query
        for row in results:
            print(row)  # Print each row from the results