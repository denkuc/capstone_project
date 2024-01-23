from typing import List

import pandas as pd


def transits_dropdown(transits: pd.DataFrame) -> List:
    transits_options = [{'label': 'Select transit', 'value': 'placeholder', 'disabled': True}]
    transits_options += [
        {'value': transit['minimum_flux_id'], 'label': transit['time']}
        for index, transit in transits.iterrows()  # Example list of numeric options
    ]
    return transits_options
