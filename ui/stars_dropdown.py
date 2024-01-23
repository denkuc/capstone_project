import dash_bootstrap_components as dbc

from data_access.read.flux import get_usual_stars_for_sector


def stars_dropdown(sector, default_star):
    stars_list = get_usual_stars_for_sector(sector)
    stars_options = [{"label": "Select star", "value": "placeholder", "disabled": True}]
    stars_options += [{'label': str(star), 'value': star} for star in stars_list]
    return dbc.Select(
        id='flux-tic-dropdown',
        options=stars_options,
        value=default_star,  # Default value
        disabled=False
    )
