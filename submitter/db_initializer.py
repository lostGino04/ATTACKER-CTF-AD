import sqlite3
import os

DB_FILE = "./database.db"

def main():

    if os.path.exists(DB_FILE):
        print("Database already created!")
        return -1

    conn = sqlite3.connect(DB_FILE)

    if not conn:
        print("Unable to connect to database!")
        return -1

    query = """CREATE TABLE IF NOT EXISTS flags (
                                flag text PRIMARY KEY,
                                tick integer,
                                submitted integer
                            );"""
    
    c = conn.cursor()

    if c.execute(query):
        print("Database created successfully!")
    
    conn.close()


if __name__ == '__main__':
    main()