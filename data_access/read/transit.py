import pandas as pd

from data_access import get_db_connection


def get_transits_for_sector(sector):
    conn = get_db_connection()
    query = f"""
        SELECT t.id, minimum_flux_id, star_tic
        FROM transit t
        JOIN flux f on f.id = t.minimum_flux_id
        WHERE sector = {sector};
    """
    df = pd.read_sql_query(query, conn)

    return df
