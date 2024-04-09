import sqlite3

DB_FILE = "./database.db"

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def connect(file=DB_FILE):
    conn =  sqlite3.connect(file)
    if not conn:
        return None
    conn.row_factory = dict_factory

    return conn


def add_flag(flag, tick):

    conn = connect()
    cursor = conn.cursor()

    success = False

    try:
        query = "INSERT INTO flags (flag, tick, submitted) VALUES (?, ?, 0)"
        cursor.execute(query, (flag, tick,))
        conn.commit()
        success= True

    except Exception:
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def find_flags():

    conn = connect()
    cursor = conn.cursor()

    query = "SELECT * FROM flags WHERE submitted <> 1"
    cursor.execute(query)
    flags = cursor.fetchall()

    cursor.close()
    conn.close()

    return flags


def update_submitted(flag):

    conn = connect()
    cursor = conn.cursor()

    success = False

    try:
        query = "UPDATE flags SET submitted = 1 WHERE flag = ?"
        cursor.execute(query, (flag,))
        conn.commit()
        success= True

    except Exception as e:
        print(str(e))
        conn.rollback()
        
    cursor.close()
    conn.close()

    return success
