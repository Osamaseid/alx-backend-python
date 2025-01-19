#!/usr/bin/python3
import seed

def paginate_users(page_size, offset):
    """
    Fetch paginated users from the database
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator function for lazy loading paginated users
    """
    offset = 0
    while True:
        # Fetch a page of users
        page = paginate_users(page_size, offset)
        
        # Stop if no more users
        if not page:
            break
        
        # Yield the current page
        yield page
        
        # Move to next page
        offset += page_size