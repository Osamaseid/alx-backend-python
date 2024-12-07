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

def stream_users_in_batches(batch_size):
    """Generator that yields batches of user data from the database."""
    connection = connect_to_prodev()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    # Fetch rows in batches
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Processes each batch to filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user  # Yield users over the age of 25

# Example usage (remove this part if you don't want to execute on import)
if __name__ == "__main__":
    for user in batch_processing(50):
        print(user)