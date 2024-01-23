from data_access.execute_db_command import execute_select_command


def star_exists(star_tic):
    # Query the star_windows_info table using the provided values
    results = execute_select_command('''SELECT type FROM star WHERE tic = ?''',
                                     (star_tic,))

    # If there's a result return true, false otherwise
    return True if results else False
