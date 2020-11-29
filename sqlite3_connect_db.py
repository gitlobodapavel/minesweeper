import sqlite3

if __name__ == '__main__':
    '''RUN THUS CODE AS A SINGLE SCRIPT TO INIT SQLITE3 DATABASE'''
    conn = sqlite3.connect("db_sqlite3.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    try:
        # Создание таблицы
        cursor.execute("""CREATE TABLE users
                                  (login text, password text) """)

    except sqlite3.OperationalError:
        # table already exists
        pass
    try:
        cursor.execute("""CREATE TABLE results
                                                  (user text, level text, time text) """)
    except sqlite3.OperationalError:
        pass

else:
    conn = sqlite3.connect("db_sqlite3.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    try:
        # Создание таблицы
        cursor.execute("""CREATE TABLE users
                                      (login text, password text) """)
        cursor.execute("""CREATE TABLE results
                                            (user text, level text, time text) """)
    except sqlite3.OperationalError:
        # table already exists
        pass

    try:
        cursor.execute("""CREATE TABLE results
                                            (user text, level text, time text) """)
    except sqlite3.OperationalError:
        pass
