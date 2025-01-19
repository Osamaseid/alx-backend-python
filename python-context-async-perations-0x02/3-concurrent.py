import asyncio
import aiosqlite

async def create_sample_database():
    """
    Create a sample SQLite database with user data.
    """
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        
        # Sample user data
        users = [
            ('Alice', 35),
            ('Bob', 42),
            ('Charlie', 28),
            ('David', 45),
            ('Eve', 39),
            ('Frank', 50)
        ]
        
        await db.executemany(
            'INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)', 
            users
        )
        await db.commit()

async def async_fetch_users():
    """
    Fetch all users from the database asynchronously.
    
    :return: List of all users
    """
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            users = await cursor.fetchall()
            print("All Users:")
            for user in users:
                print(user)
            return users

async def async_fetch_older_users():
    """
    Fetch users older than 40 from the database asynchronously.
    
    :return: List of users older than 40
    """
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers Older than 40:")
            for user in older_users:
                print(user)
            return older_users

async def fetch_concurrently():
    """
    Execute both user fetch queries concurrently using asyncio.gather.
    
    :return: Tuple of query results
    """
    # Ensure database is created before queries
    await create_sample_database()
    
    # Use asyncio.gather to run queries concurrently
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    return results

def main():
    """
    Run the concurrent database queries.
    """
    # Run the concurrent fetch using asyncio.run
    results = asyncio.run(fetch_concurrently())
    
    # Optionally process or display results
    all_users, older_users = results
    print("\nQuery Results Summary:")
    print(f"Total Users: {len(all_users)}")
    print(f"Users Older than 40: {len(older_users)}")

if __name__ == '__main__':
    main()
