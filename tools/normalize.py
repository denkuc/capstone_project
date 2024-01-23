import os

import lightkurve as lk
import numpy as np
from astropy.io import fits

from data_access import get_data_folder
from data_access.read.sector import get_file_name_pattern_of_sector


def get_sector_data_folder(sector: int) -> str:
    # Converts the sector number to a zero-padded string
    sector_str = str(sector).zfill(2)

    # Constructs the folder name
    folder_name = f'TESS_fits_s{sector_str}'

    # Creates the full path
    full_path = os.path.join(get_data_folder(), folder_name)

    return full_path


def get_tic_index_from_full_name(full_name: str) -> int:
    return int(os.path.basename(full_name).split('-')[2])


def get_full_path_for_tic(sector: int, tic: str) -> str:
    folder = get_sector_data_folder(sector)

    file_name_pattern = get_file_name_pattern_of_sector(sector)
    file_name = file_name_pattern.format(tic.zfill(16))

    return os.path.join(folder, file_name)


def create_normalized_light_curve_from_fits(sector: int, tic: str) -> lk.LightCurve:
    """to create lightkurve from fits file"""
    path = get_full_path_for_tic(sector, tic)
    hdu = fits.open(path)

    # Read the flux and time data, ensuring that they are finite numbers
    fluxes = np.array(hdu[1].data['SAP_FLUX'], dtype=np.float64)
    times = np.array(hdu[1].data['TIME'], dtype=np.float64)

    # normalize the lc
    normalized_lc = create_light_curve_from_numpy(fluxes, times).normalize()

    return normalized_lc


def create_light_curve_from_numpy(fluxes: np.array, times: np.array) -> lk.LightCurve:
    # Filter out non-finite values from both fluxes and times
    finite_indices = np.isfinite(times) & np.isfinite(fluxes)
    filtered_fluxes = fluxes[finite_indices]
    filtered_times = times[finite_indices]

    # Create the LightCurve object
    return lk.LightCurve(time=filtered_times, flux=filtered_fluxes)
