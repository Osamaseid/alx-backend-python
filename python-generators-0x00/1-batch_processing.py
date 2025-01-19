#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function to stream users from the database in batches
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='afsaaef',
        database='ALX_prodev'
    )
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM user_data")
        
        batch = []
        for row in cursor:
            batch.append(row)
            
            if len(batch) == batch_size:
                yield batch
                batch = []
        
        if batch:
            yield batch
    
    finally:
        cursor.close()
        connection.close()

def batch_processing(batch_size=50):
    """
    Process users in batches, filtering users over 25 years old
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)