import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Output, Input, dash

from data_access.read.flux import get_raw_flux_for_star_in_sector
from data_access.read.flux_stat import retrieve_sector_stats
from ui.sectors_dropdown import sectors_dropdown

statistics_options = ['mean', 'std', 'max', 'min', 'range', 'beyond1std', 'amplitude']
sectors_dashboard = html.Div([
    html.Table([
        html.Tr([
            html.Td(
                # Insert tables or other elements in the sidebar here
                html.Table([
                    html.Tr([html.Td('Sector:'),
                             html.Td(sectors_dropdown(5))]),
                    html.Tr([html.Td('X-Axis Statistics:'),
                             html.Td(dcc.Dropdown(statistics_options, 'min', id='x-dropdown', style={'width': '60px'},))]),
                    html.Tr([html.Td('Y-Axis Statistics:'),
                             html.Td(dcc.Dropdown(statistics_options, 'std', id='y-dropdown', style={'width': '60px'},))])
                ])
            ),

            # Main content area on the right
            html.Td(
                html.Div([
                    # Main content area
                    dcc.Graph(id='stats-content'),
                ]), style={'width': '85%'})
        ])
    ], style={'width': '100%'}),
    html.Div(
        [
            dcc.Graph(id='flux-content')
        ],
        id='flux-display',
        style={'display': 'none'}
    )
])


@callback(
    Output('stats-content', 'figure'),
    Input('sector-dropdown', 'value'),
    Input('x-dropdown', 'value'),
    Input('y-dropdown', 'value')
)
def update_statistics_comparison(sector, x_axis_stat, y_axis_stat):
    sector_stats = retrieve_sector_stats(sector, x_axis_stat, y_axis_stat)
    df = pd.DataFrame(sector_stats, columns=['tic', x_axis_stat, y_axis_stat, 'type', 'has_planets'])

    if x_axis_stat != y_axis_stat:
        fig = px.scatter(df,
                         x=x_axis_stat,
                         y=y_axis_stat,
                         color='type',
                         hover_name=df['tic'],
                         symbol='has_planets',
                         symbol_map={0: 'circle', 1: 'triangle-up'})
        fig.update_traces(marker=dict(size=8, opacity=.6))
    else:
        fig = px.histogram(df, x=x_axis_stat)

    return fig


@callback(
    Output('flux-display', 'style'),
    Output('flux-content', 'figure'),
    Input('stats-content', 'clickData'),
    Input('sector-dropdown', 'value'),
)
def update_flux(click_data, sector):
    if not click_data:
        flux_display_style = {'display': 'none'}
        return flux_display_style, dash.no_update

    sector = int(sector)
    star_tic = click_data['points'][0]['hovertext']

    df = get_raw_flux_for_star_in_sector(sector, star_tic)
    fig = px.scatter(x=df.time, y=df.flux, title=f'Whole flux - {star_tic}, Sector - {sector}')
    fig.update_traces(marker=dict(size=5, opacity=.6))

    flux_display_style = {'height': '40%', 'width': '100%', 'display': 'inline-block'}

    return flux_display_style, fig
