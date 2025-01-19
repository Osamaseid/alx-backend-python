#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    """
    Generator to yield user ages one by one
    """
    # Establish database connection
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',  # Replace with your MySQL username
        password='your_password',  # Replace with your MySQL password
        database='ALX_prodev'
    )
    
    # Create cursor
    cursor = connection.cursor()
    
    try:
        # Execute query to fetch user ages
        cursor.execute("SELECT age FROM user_data")
        
        # Yield ages one by one
        for (age,) in cursor:
            yield age
    
    finally:
        # Ensure cursor and connection are closed
        cursor.close()
        connection.close()

def calculate_average_age():
    """
    Calculate average age using generator
    """
    total_age = 0
    user_count = 0
    
    # Stream and aggregate ages
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    # Calculate and print average
    average_age = total_age / user_count if user_count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")

# Run the calculation
if __name__ == "__main__":
    calculate_average_age()