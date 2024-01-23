import os

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from ui import NOTEBOOKS_FOLDER_PATH, IMAGE_FOLDER_PATH
from ui.visualization.main_page import main_page_dashboard
from ui.visualization.sectors import sectors_dashboard
from ui.visualization.stars import stars_dashboard

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)


# Logo as html.Img component
logo = html.Img(src=IMAGE_FOLDER_PATH + "logo.png", height="40px")
# Define the navigation panel
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Notebooks", href=NOTEBOOKS_FOLDER_PATH, target="_blanc")),
        dbc.NavItem(dbc.NavLink("Sectors", href="/sectors")),
        dbc.NavItem(dbc.NavLink("Stars", href="/stars")),
    ],
    brand=logo,
    brand_href="/",
    color="#001012",
    dark=True,
)


# Common layout structure
def serve_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        navbar,
        html.Div(id='page-content', style={'padding-left': '5%', 'padding-right': '5%', 'padding-top': '15px'})
    ])


app.layout = serve_layout


# Callback to switch content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return main_page_dashboard
    elif pathname == '/sectors':
        return sectors_dashboard
    elif pathname == '/stars':
        return stars_dashboard
    else:
        return '404 Page Not Found'


if __name__ == '__main__':
    app.run_server(debug=False, port=os.getenv('DASH_APP_PORT'))
