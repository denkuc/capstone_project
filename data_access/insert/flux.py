import lightkurve as lk
import pandas as pd

from data_access import get_db_connection


def insert_flux(sector: int, star_tic: str, light_curve: lk.LightCurve):
    # Insert the provided values into the observation table
    df = pd.DataFrame({
        'sector': sector,
        'star_tic': star_tic,
        'time': light_curve.time.value,
        'flux': light_curve.flux.value
    })
    conn = get_db_connection()
    df.to_sql('flux', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()


def insert_flux_trend_and_ma(df: pd.DataFrame):
    conn = get_db_connection()
    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute(
            'UPDATE flux SET trend_flux = ?, m_a_trend_flux = ? WHERE id = ?',
            (row['trend_flux'], row['m_a_trend_flux'], index)
        )
    conn.commit()
    conn.close()
