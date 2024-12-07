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