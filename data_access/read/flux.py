import pandas as pd

from data_access import get_db_connection
from data_access.execute_db_command import execute_select_command


def flux_exists(sector: int, star_tic: str):
    # Query the star_windows_info table using the provided values
    results = execute_select_command('''SELECT id 
                                        FROM flux 
                                        WHERE sector = ? AND star_tic = ?''',
                                     (sector, star_tic))

    # If there's a result return true, false otherwise
    return True if results else False


def get_raw_flux_for_star_in_sector(sector, star_tic):
    conn = get_db_connection()
    query = f"""
    SELECT id, time, flux
    FROM flux
    WHERE sector = {sector}
      AND star_tic = {star_tic};
    """
    df = pd.read_sql_query(query, conn, index_col='id')

    return df


def get_m_a_trend_flux_for_star_in_sector(sector, star_tic):
    conn = get_db_connection()
    query = f"""
    SELECT id, time, m_a_trend_flux
    FROM flux
    WHERE sector = {sector}
      AND star_tic = {star_tic};
    """
    df = pd.read_sql_query(query, conn, index_col='id')

    return df


def get_all_flux_and_transits_info_for_star_in_sector(sector, star_tic):
    conn = get_db_connection()
    query = f"""
    SELECT f.id as f_id, sector, star_tic, time, flux, trend_flux, m_a_trend_flux, t.id as t_id, minimum_flux_id, start_flux_id, end_flux_id, width_left, width_right, m_a_trend_depth_left, m_a_trend_depth_right
    FROM flux f
    LEFT JOIN transit t on f.id = t.minimum_flux_id
    WHERE sector = {sector}
      AND star_tic = {star_tic};
    """
    df = pd.read_sql_query(query, conn, index_col='f_id')

    return df


def get_usual_stars_for_sector(sector):
    results = execute_select_command('''SELECT DISTINCT star_tic 
                                        FROM flux
                                        JOIN star s on flux.star_tic = s.tic
                                        WHERE sector = ? and type in ('Star', 'High Proper Motion Star')''',
                                     (sector, ))

    star_tics = [result[0] for result in results]

    return star_tics


def get_all_stars_for_sector(sector):
    results = execute_select_command('''SELECT DISTINCT star_tic 
                                        FROM flux
                                        WHERE sector = ?''',
                                     (sector, ))

    star_tics = [result[0] for result in results]

    return star_tics
