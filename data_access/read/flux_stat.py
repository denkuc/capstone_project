from data_access.execute_db_command import execute_select_command


def retrieve_sector_stats(sector, first_stat, second_stat):
    # Query the flux_stat table using the provided sector value
    query = f'''
       SELECT star_tic, {first_stat}, {second_stat}, s.type, s.has_planets
       FROM flux_stat fs
       LEFT JOIN star s on fs.star_tic = s.tic
       WHERE sector = ?
       '''

    # Fetch all the results
    results = execute_select_command(query, (sector,))

    return results
