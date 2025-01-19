import sqlite3

class DatabaseConnection:
    """
    Custom context manager for database connections
    """
    def __init__(self, db_name='users.db'):
        """
        Initialize the database connection
        
        Args:
            db_name (str): Name of the SQLite database file
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Establish database connection when entering the context
        
        Returns:
            sqlite3.Cursor: Database cursor for executing queries
        """
        # Open connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close database connection when exiting the context
        
        Args:
            exc_type: Exception type (if any)
            exc_value: Exception value (if any)
            traceback: Traceback object (if any)
        """
        # Close cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

def main():
    """
    Demonstrate usage of DatabaseConnection context manager
    """
    # Use context manager to execute a query
    with DatabaseConnection() as cursor:
        # Execute query to select all users
        cursor.execute("SELECT * FROM users")
        
        # Fetch and print results
        users = cursor.fetchall()
        for user in users:
            print(user)

if __name__ == "__main__":
    main()
