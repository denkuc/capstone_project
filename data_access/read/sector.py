from data_access.execute_db_command import execute_select_command


def get_sectors_with_data():
    # Query the star_windows_info table using the provided values
    results = execute_select_command("""SELECT id FROM sector WHERE file_name_pattern != ''""")
    # If there's a result, convert the comma-separated string back to a list of floats
    sectors_ids = [result[0] for result in results]

    return sectors_ids


def get_file_name_pattern_of_sector(sector: int) -> str:
    results = execute_select_command('''SELECT file_name_pattern FROM sector WHERE id = ?''', (sector,))

    return results[0][0]
