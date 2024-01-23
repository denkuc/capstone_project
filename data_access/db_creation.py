import os.path

import pandas as pd

from data_access import get_db_connection, get_data_folder
from data_access.insert.sector import insert_sectors
from data_access.insert.star import insert_stars

# Create a new SQLite database or connect to an existing one
conn = get_db_connection()
cursor = conn.cursor()

# Create the sector table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sector (
    id INTEGER PRIMARY KEY,
    file_name_pattern TEXT,
    start_time REAL,
    end_time REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS star (
    tic INTEGER PRIMARY KEY,
    type TEXT,
    has_planets INTEGER DEFAULT 0
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS flux (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector INTEGER,
    star_tic INTEGER,
    time REAL,
    flux REAL,
    trend_flux REAL,
    m_a_trend_flux REAL,
    FOREIGN KEY(star_tic) REFERENCES star(tic),
    FOREIGN KEY(sector) REFERENCES sector(id)
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS flux_stat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector INTEGER,
    star_tic INTEGER,
    mean FLOAT,
    max FLOAT,
    min FLOAT,
    std FLOAT,
    range FLOAT,
    amplitude FLOAT,
    beyond1std FLOAT,
    FOREIGN KEY(star_tic) REFERENCES star(tic),
    FOREIGN KEY(sector) REFERENCES sector(id)
);''')

cursor.execute('''
CREATE INDEX IF NOT EXISTS idx_sector_star_tic ON flux (sector, star_tic);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    minimum_flux_id INTEGER UNIQUE,
    start_flux_id INTEGER,
    end_flux_id INTEGER,
    width_left REAL,
    width_right REAL,
    m_a_trend_depth_left REAL,
    m_a_trend_depth_right REAL,
    FOREIGN KEY(minimum_flux_id) REFERENCES flux(id),
    FOREIGN KEY(start_flux_id) REFERENCES flux(id),
    FOREIGN KEY(end_flux_id) REFERENCES flux(id)
);''')
# Commit the changes and close the connection
conn.commit()
conn.close()

# Populate DB with Default values
data_folder = get_data_folder()
# Insert sectors data
sectors_df = pd.read_excel(os.path.join(data_folder, 'sectors.xlsx'), header=0, index_col=0)
insert_sectors(sectors_df)

# Insert stars data
stars_df = pd.read_excel(os.path.join(data_folder, 'exoplanets.xlsx'), header=0, usecols=[0])
insert_stars(stars_df)
