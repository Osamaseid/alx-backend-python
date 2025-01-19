#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator function to stream users from the database one by one
    """
    # Establish database connection
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='dsjtrstj',
        database='ALX_prodev'
    )
    
    # Create cursor
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Execute query to fetch all users
        cursor.execute("SELECT * FROM user_data")
        
        # Yield rows one by one
        for row in cursor:
            yield row
    
    finally:
        # Ensure cursor and connection are closed
        cursor.close()
        connection.close()