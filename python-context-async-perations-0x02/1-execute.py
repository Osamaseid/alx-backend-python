import sqlite3

class ExecuteQuery:
    """
    A context manager for executing database queries safely and efficiently.
    
    This class manages database connection and query execution, ensuring 
    proper resource management and exception handling.
    """
    
    def __init__(self, database_path, query, params=None):
        """
        Initialize the context manager with database path, query, and optional parameters.
        
        :param database_path: Path to the SQLite database file
        :param query: SQL query to be executed
        :param params: Optional tuple of parameters for parameterized queries
        """
        self.database_path = database_path
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """
        Establish database connection and execute the query.
        
        :return: Results of the query
        """
        try:
            # Establish a connection to the database
            self.connection = sqlite3.connect(self.database_path)
            self.cursor = self.connection.cursor()
            
            # Execute the query with parameters
            self.cursor.execute(self.query, self.params)
            
            # Fetch all results
            self.results = self.cursor.fetchall()
            
            return self.results
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close cursor and connection, handling any potential exceptions.
        
        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return: False to propagate exceptions, True to suppress
        """
        if self.cursor:
            self.cursor.close()
        
        if self.connection:
            self.connection.close()
        
        # Propagate any exceptions that occurred
        return False

# Example usage
def main():
    # Create a sample database for demonstration
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER
        )
    ''')
    
    # Insert some sample data
    sample_users = [
        ('Alice', 30),
        ('Bob', 25),
        ('Charlie', 35),
        ('David', 22)
    ]
    
    cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', sample_users)
    conn.commit()
    conn.close()

    # Demonstrate the context manager usage
    with ExecuteQuery('users.db', 'SELECT * FROM users WHERE age > ?', (25,)) as results:
        if results:
            print("Users older than 25:")
            for user in results:
                print(user)

if __name__ == '__main__':
    main()
