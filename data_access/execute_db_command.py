import sqlite3

from data_access import get_db_path


def execute_insert_command(command, parameters=None):
    # Connect to the SQLite database
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    if parameters:
        cursor.execute(command, parameters)
    else:
        cursor.execute(command)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def execute_select_command(command, parameters=None):
    # Connect to the SQLite database
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    if parameters:
        cursor.execute(command, parameters)
    else:
        cursor.execute(command)

    # Fetch the result
    results = cursor.fetchall()

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return results
