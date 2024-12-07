import mysql.connector
import os
from seed import connect_to_prodev

def stream_user_ages():
    """Generator that yields user ages from the user_data table one by one."""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")

    for row in cursor:
        yield row['age']  # Yield each user's age

    cursor.close()
    connection.close()

def calculate_average_age():
    """Calculates the average age of users using the stream_user_ages generator."""
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age  # Sum the ages
        count += 1  # Count the number of users

    if count == 0:
        return 0  # Avoid division by zero

    average_age = total_age / count  # Calculate the average
    return average_age

if __name__ == "__main__":
    average = calculate_average_age()
    print(f"Average age of users: {average}")