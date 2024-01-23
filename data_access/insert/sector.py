import pandas as pd

from data_access import get_db_connection
from data_access.execute_db_command import execute_insert_command


def insert_file_name_pattern_to_sector(sector: int, file_name_pattern: str):
    execute_insert_command('''UPDATE sector SET file_name_pattern=? WHERE id=? ''', (file_name_pattern, sector))


def insert_sectors(sectors_df: pd.DataFrame):
    df = pd.DataFrame({
        'id': sectors_df.index,
        'file_name_pattern': '',
        'start_time': sectors_df['StartTJD'],
        'end_time': sectors_df['EndTJD'],
    })
    conn = get_db_connection()
    df.to_sql('sector', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
