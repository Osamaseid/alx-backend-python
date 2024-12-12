import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
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
                return self.connection.cursor()  # Return a cursor for executing queries
        except Error as e:
            print(f"Error: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the database connection
        if self.connection and self.connection.is_connected():
            self.connection.close()

# Example usage
if __name__ == "__main__":
    with DatabaseConnection('localhost', 'root', '123456', 'alx-backend-python') as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()  # Fetch all results from the executed query
        for row in results:
            print(row)