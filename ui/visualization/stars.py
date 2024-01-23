import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback, Output, Input, State, ctx, dash
from plotly.graph_objs import Scatter, Figure

from data_access.read.flux import get_all_flux_and_transits_info_for_star_in_sector
from ui import IMAGE_FOLDER_PATH
from ui.sectors_dropdown import sectors_dropdown
from ui.stars_dropdown import stars_dropdown
from ui.transit_params_table import transit_params_table
from ui.transits_dropdown import transits_dropdown

default_sector = 5
default_star = '270577175'  # Beta-Pictoris

stars_dashboard = html.Div([
    html.Div(
        [
            html.Table([
                html.Td(html.Label('Sector:')),
                html.Td(sectors_dropdown(default_sector), style={'padding-right': '10px'}),
                html.Td(html.Label('Star TIC:')),
                html.Td(stars_dropdown(default_sector, default_star), style={'padding-right': '10px'}),
                html.Td(dbc.Button('Show a star', id='flux-tic-button')),
            ], style={'marginLeft': 'auto', 'marginRight': 'auto', 'marginTop': '4px'}),
            html.Div(html.A([
                'Look at the star in ',
                html.Img(src=IMAGE_FOLDER_PATH+'simbad.jpg', style={'width': '45px', 'height': '20px'})
            ], id='star-link', target="_blank", href="/stars")),
            dcc.Graph(id='star-plot')
        ],
        style={'height': '25%', 'width': '100%', 'display': 'inline-block'}
    ),
    html.Div(
        [
            html.Div([
                html.Div(
                    dbc.Select(
                        id='transit-select',
                        options=[]
                    ),
                    style={'display': 'inline-block', 'vertical-align': 'top'}
                )
            ], style={'display': 'flex', 'align-items': 'center'}),
            dcc.Graph(id='transit-plot', style={'display': 'inline-block', 'flex-grow': 1}),
            html.Div([], id='transit-table-holder', style={'margin-left': 'auto'})
        ],
        id='transit-display',
        style={'display': 'none'}
    ),

])


def trend_scatter(dataframe: pd.DataFrame) -> Scatter:
    return Scatter(x=dataframe.time, y=dataframe.trend_flux, name='Trend flux', mode='markers',
                   marker={'size': 2, 'opacity': .8, 'color': 'red'})


def moving_average_trend_scatter(dataframe: pd.DataFrame) -> Scatter:
    return Scatter(x=dataframe.time, y=dataframe.m_a_trend_flux, name='Moving average trend flux', mode='markers',
                   marker={'size': 2, 'opacity': .8, 'color': 'green'})


def transit_point_scatter(points: pd.DataFrame, point_type: str, point_marker: str) -> Scatter:
    return Scatter(x=points.time, y=points.m_a_trend_flux, name=f'Potential transit {point_type}', mode='markers',
                   marker={'size': 12, 'opacity': 1, 'color': 'blue', 'symbol': point_marker})


def transit_minima_scatter(points: pd.DataFrame) -> Scatter:
    return transit_point_scatter(points, 'minimum', 'x')


def transit_ingress_scatter(points: pd.DataFrame) -> Scatter:
    return transit_point_scatter(points, 'ingress', 'triangle-right')


def transit_egress_scatter(points: pd.DataFrame) -> Scatter:
    return transit_point_scatter(points, 'egress', 'triangle-left')


def figure_for_transit(whole_df: pd.DataFrame, transits: pd.DataFrame) -> Figure:
    transit_df = transits.iloc[0]
    start_flux_id = int(transit_df['start_flux_id'])
    end_flux_id = int(transit_df['end_flux_id'])
    df_filtered = whole_df.loc[start_flux_id - 50:end_flux_id + 50, :]
    fig = Figure()
    fig.add_trace(trend_scatter(df_filtered))
    fig.add_trace(moving_average_trend_scatter(df_filtered))
    fig.add_trace(transit_minima_scatter(transits))
    ingress_points = whole_df[whole_df.index == start_flux_id]
    fig.add_trace(transit_ingress_scatter(ingress_points))
    egress_points = whole_df[whole_df.index == end_flux_id]
    fig.add_trace(transit_egress_scatter(egress_points))

    return fig


@callback(
    Output('star-plot', 'figure'),
    Output('star-link', 'href'),
    Output('transit-display', 'style'),
    Output('transit-select', 'options'),
    Output('transit-select', 'value'),
    Output('transit-plot', 'figure'),
    Output('transit-table-holder', 'children'),
    [Input('flux-tic-button', 'n_clicks'),
     Input('transit-select', 'value')],
    [State('sector-dropdown', 'value'),
     State('flux-tic-dropdown', 'value')]
)
def update_star_plots(n_clicks, transit_selected_minimum_flux_id, sector, star_tic):
    df = get_all_flux_and_transits_info_for_star_in_sector(sector, star_tic)
    if ctx.triggered[0]['prop_id'] == 'flux-tic-button.n_clicks' and (n_clicks is None or n_clicks > 0):
        transits = df[df['minimum_flux_id'].notna()]

        fig1 = Figure()
        fig1.add_trace(Scatter(x=df.time, y=df.flux, name='Raw flux', mode='markers',
                               marker={'size': 2, 'opacity': .2, 'color': 'black'}))
        fig1.add_trace(trend_scatter(df))
        fig1.add_trace(moving_average_trend_scatter(df))
        fig1.add_trace(transit_minima_scatter(transits))
        fig1.update_layout(title=f'Flux for star TIC {star_tic} in Sector #{sector}')
        
        star_link = f'https://simbad.u-strasbg.fr/simbad/sim-basic?Ident=TIC{star_tic}&submit=SIMBAD+search'
        
        if not transits.empty:
            transits_display = {
                'display': 'flex',
                'height': '25%',
                'align-items': 'center',
                'justify-content': 'space-between',
                'padding-left': '10%',
                'padding-right': '10%'
            }
            transits_options = transits_dropdown(transits)
            transits_value = transits_options[0]['value']
            transits = transits.head(1)
            fig2 = figure_for_transit(df, transits)
            transit_table = transit_params_table(df, transits)

            return fig1, star_link, transits_display, transits_options, transits_value, fig2, transit_table

        transits_display = {'display': 'none'}

        return fig1, star_link, transits_display, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    elif ctx.triggered[0]['prop_id'] == 'transit-select.value':
        transits = df[df.index == int(transit_selected_minimum_flux_id)]
        fig = figure_for_transit(df, transits)
        transit_table = transit_params_table(df, transits)

        # As this callback is only updating the transit plot,
        # other outputs can remain unchanged by returning dash.no_update
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, fig, transit_table

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
