import pandas as pd
from astropy.time import Time
from wotan import flatten


def add_wotan_trend(df: pd.DataFrame, window_length: float = 0.3):
    _, trend_flux = flatten(
        time=df.time.values,  # Array of time values
        flux=df.flux.values,  # Array of flux values
        method='biweight',
        window_length=window_length,  # The length of the filter window in units of ``time``
        break_tolerance=.5,  # Split into segments at breaks longer than that
        return_trend=True,  # Return trend and flattened light curve
        cval=5.0  # Tuning parameter for the robust estimators
    )
    df['trend_flux'] = trend_flux
