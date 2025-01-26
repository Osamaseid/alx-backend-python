import mysql.connector
import os

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),          # Get from environment variable
            user=os.getenv('DB_USER'),          # Get from environment variable
            password=os.getenv('DB_PASSWORD'),   # Get from environment variable
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def stream_users():
    """Generator that streams rows from the user_data table one by one."""
    connection = connect_to_prodev()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)  # Use dictionary for easy row access
    cursor.execute("SELECT * FROM user_data;")

    # Use a single loop to yield rows
    for row in cursor:
        yield row  # Yield each row one by one

    cursor.close()
    connection.close()