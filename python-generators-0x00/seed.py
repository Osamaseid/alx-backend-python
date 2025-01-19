#!/usr/bin/python3
import mysql.connector
import csv
import uuid

def connect_db():
    """
    Connects to the MySQL server
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mishakmosi'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL Server: {err}")
        return None

def create_database(connection):
    """
    Creates the ALX_prodev database if it doesn't exist
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
        return False

def connect_to_prodev():
    """
    Connects to the ALX_prodev database
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mishakmosi',
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None

def create_table(connection):
    """
    Creates the user_data table if it doesn't exist
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10,0) NOT NULL,
            UNIQUE KEY (email)
        )
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
        return False

def insert_data(connection, csv_file):
    """
    Inserts data from CSV file into user_data table
    """
    try:
        cursor = connection.cursor()
        
        # Read CSV and insert data
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            
            for row in csv_reader:
                # Generate UUID if not provided in CSV
                user_id = str(uuid.uuid4()) if not row[0] else row[0]
                name = row[1]
                email = row[2]
                age = row[3]
                
                # Insert or ignore if duplicate
                insert_query = """
                INSERT IGNORE INTO user_data 
                (user_id, name, email, age) 
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, name, email, age))
        
        connection.commit()
        print(f"Data from {csv_file} inserted successfully")
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        return False