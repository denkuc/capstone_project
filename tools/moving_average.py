import numpy as np
import pandas as pd


def get_index_half_window_size(df: pd.DataFrame, window_size_in_steps: int):
    """ Calculate the index half window size based on time step difference """
    one_step_time_difference = df.time.values[1] - df.time.values[0]
    window_size = window_size_in_steps * one_step_time_difference
    half_window_size = window_size / 2

    return int(half_window_size / one_step_time_difference)


def add_moving_averages(df: pd.DataFrame, window_size_in_steps: int):
    index_half_window_size = get_index_half_window_size(df, window_size_in_steps)

    flux_values = df.trend_flux
    flux_values_len = len(flux_values)

    # Iterate over the time_values to calculate the centered rolling average for each point
    moving_averages = []
    for i in range(flux_values_len):
        # Determine the start and end indices for the current window
        start_idx = max(i - index_half_window_size, 0)
        end_idx = min(i + index_half_window_size, flux_values_len - 1)

        # Calculate the average for the window
        window_fluxes = flux_values[start_idx:end_idx + 1]
        moving_averages.append(np.mean(window_fluxes))

    df['m_a_trend_flux'] = moving_averages
