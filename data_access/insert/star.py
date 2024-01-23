import pandas as pd

from data_access import get_db_connection
from data_access.execute_db_command import execute_insert_command
from data_access.read.star import star_exists


def insert_star_type(star_tic, star_type):
    if star_exists(star_tic):
        execute_insert_command('''UPDATE star
                                  SET type=?
                                  WHERE tic=?''', (star_type, star_tic))

    execute_insert_command('''INSERT INTO star (tic, type) 
                              VALUES (?, ?)''',
                           (star_tic, star_type))


def insert_stars(stars_df: pd.DataFrame):
    conn = get_db_connection()
    cursor = conn.cursor()
    for index, row in stars_df.iterrows():
        cursor.execute('''INSERT OR IGNORE INTO star (tic, has_planets)
                          VALUES (?, ?)''', (int(row['TIC ID']), 1))
    conn.commit()
    conn.close()
