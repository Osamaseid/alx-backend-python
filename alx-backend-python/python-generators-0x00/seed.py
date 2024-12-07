import os
import mysql.connector
import csv
import uuid

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),          
            user=os.getenv('DB_USER'),          
            password=os.getenv('DB_PASSWORD')   
        )
        print("Connected to MySQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),          
            user=os.getenv('DB_USER'),          
            password=os.getenv('DB_PASSWORD'),   
            database='ALX_prodev'
        )
        print("Connected to ALX_prodev database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3, 0) NOT NULL
    );
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    """Inserts data from the CSV file into the database."""
    cursor = connection.cursor()
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())  # Generate a new UUID
            name = row['name']
            email = row['email']
            age = row['age']
            insert_query = """
            INSERT INTO user_data (user_id, name, email, age) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                name = VALUES(name), 
                email = VALUES(email), 
                age = VALUES(age);
            """
            try:
                cursor.execute(insert_query, (user_id, name, email, age))
            except mysql.connector.Error as err:
                print(f"Failed inserting data: {err}")
    connection.commit()
    print("Data inserted successfully.")
    cursor.close()

def stream_rows(connection):
    """Generator that streams rows from the user_data table one by one."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    for row in cursor:
        yield row
    cursor.close()

# Example usage (remove this part if you don't want to execute on import)
if __name__ == "__main__":
    db_connection = connect_db()
    if db_connection:
        create_database(db_connection)
        db_connection.close()

    # Connect to the new database
    db_connection = connect_to_prodev()
    if db_connection:
        create_table(db_connection)
        insert_data(db_connection, 'user_data.csv')

        # Streaming rows
        for user in stream_rows(db_connection):
            print(user)

        db_connection.close()