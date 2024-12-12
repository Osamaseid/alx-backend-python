import mysql.connector
from mysql.connector import Error

class ExecuteQuery:
    def __init__(self, host, user, password, database, query, params):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.query = query
        self.params = params
        self.connection = None

    def __enter__(self):
        # Open the database connection
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(self.query, self.params)  # Execute the query with parameters
                results = cursor.fetchall()  # Fetch all results
                cursor.close()  # Close the cursor
                return results  # Return the results
        except Error as e:
            print(f"Error: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the database connection
        if self.connection and self.connection.is_connected():
            self.connection.close()

# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)  # Parameters must be a tuple

    with ExecuteQuery('localhost', 'root', '12345678', 'alx-backend-python', query, params) as results:
        for row in results:
            print(row)