import dash_bootstrap_components as dbc

from data_access.read.sector import get_sectors_with_data


def sectors_dropdown(default_sector: int = 0):
    sectors_list = get_sectors_with_data()
    sectors_options = [{"label": "Select sector", "value": "placeholder", "disabled": True}]
    sectors_options += [{'label': str(sector), 'value': sector} for sector in sectors_list]

    return dbc.Select(
        id='sector-dropdown',
        options=sectors_options,
        value=default_sector,  # Default value
        style={'width': '60px'},
        disabled=False  # Default value
    )
