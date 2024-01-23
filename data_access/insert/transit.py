import pandas as pd

from data_access import get_db_connection


def insert_transit_windows(flux_df: pd.DataFrame):
    conn = get_db_connection()
    cursor = conn.cursor()
    for _, row in flux_df.iterrows():
        minimum_flux_id = row['db_id']
        start_flux_id = row['transit_start_flux_id']
        end_flux_id = row['transit_end_flux_id']
        width_left = row['width_of_biggest_neg_trend_to_left']
        width_right = row['width_of_biggest_pos_trend_to_right']
        depth_left = row['transit_depth_left']
        depth_right = row['transit_depth_right']
        cursor.execute(
            '''INSERT OR IGNORE INTO transit 
               (minimum_flux_id, start_flux_id, end_flux_id, width_left, width_right, m_a_trend_depth_left, m_a_trend_depth_right) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (minimum_flux_id, start_flux_id, end_flux_id, width_left, width_right, depth_left, depth_right)
        )
    conn.commit()
    conn.close()


def update_transit_windows(transit_series: pd.Series):
    conn = get_db_connection()
    cursor = conn.cursor()

    minimum_flux_id = transit_series['minimum_flux_id']
    start_flux_id = transit_series['transit_start_flux_id']
    end_flux_id = transit_series['transit_end_flux_id']
    width_left = transit_series['width_of_biggest_neg_trend_to_left']
    width_right = transit_series['width_of_biggest_pos_trend_to_right']
    depth_left = transit_series['transit_depth_left']
    depth_right = transit_series['transit_depth_right']

    cursor.execute(
        '''
        UPDATE transit 
        SET start_flux_id=?, end_flux_id=?, width_left=?, width_right=?, m_a_trend_depth_left=?, m_a_trend_depth_right=? 
        WHERE minimum_flux_id=?''',
        (start_flux_id, end_flux_id, width_left, width_right, depth_left, depth_right, minimum_flux_id)
    )
    conn.commit()
    conn.close()
