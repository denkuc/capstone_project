import os
import sqlite3


def get_data_folder() -> str:
    # Retrieve BASE_PATH from the environment variables
    base_path = os.getenv('BASE_EXOCODE_PATH')

    return os.path.join(base_path, 'data')


def get_db_path() -> str:
    return os.path.join(get_data_folder(), 'star_data.db')


def get_db_connection():
    db_path = get_db_path()
    return sqlite3.connect(db_path)
