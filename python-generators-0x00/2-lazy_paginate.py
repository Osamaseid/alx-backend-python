import mysql.connector
import os
from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """Fetches a page of users from the database."""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """Generator that lazily loads paginated data from the user_data table."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)  # Fetch the next page
        if not page:  # If there are no more rows, stop the generator
            break
        yield page  # Yield the current page
        offset += page_size  # Move to the next offset