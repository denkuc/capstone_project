from data_access.execute_db_command import execute_insert_command


def insert_flux_stats(sector, star_tic, mean, flux_max, flux_min, std, flux_range, amplitude, beyond1std):
    execute_insert_command(
        '''INSERT INTO flux_stat (sector, star_tic, mean, max, min, std, range, amplitude, beyond1std)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (sector, star_tic, mean, flux_max, flux_min, std, flux_range, amplitude, beyond1std)
    )
