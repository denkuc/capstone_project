import pandas as pd
from dash import html
import dash_bootstrap_components as dbc


def transit_params_table(whole_df: pd.DataFrame, transit: pd.DataFrame) -> html.Table:
    transit = transit.iloc[0]

    def get_time_value(point_column_name: str) -> float:
        return whole_df[whole_df.index == int(transit[point_column_name])]['time'].values[0]

    ingress_value = get_time_value('start_flux_id')
    minimum_value = get_time_value('minimum_flux_id')
    egress_value = get_time_value('end_flux_id')
    transit_width = egress_value - ingress_value
    entering_width = minimum_value - ingress_value
    exiting_width = egress_value - minimum_value
    depth_ingress_value = transit['m_a_trend_depth_left']
    depth_egress_value = transit['m_a_trend_depth_right']

    return dbc.Table([
        # Table header
        html.Thead(
            html.Tr([html.Th("Transit parameter"), html.Th("Value")], className="table-primary")
        ),
        # Table body
        html.Tbody([
            html.Tr([html.Td("Ingress point (t)"), html.Td(ingress_value)]),
            html.Tr([html.Td("Minimum point (t)"), html.Td(minimum_value)]),
            html.Tr([html.Td("Egress point (t)"), html.Td(egress_value)]),
            html.Tr([html.Td("Transit width (t)"), html.Td(transit_width)]),
            html.Tr([html.Td("Entering width (t)"), html.Td(entering_width)]),
            html.Tr([html.Td("Exiting width (t)"), html.Td(exiting_width)]),
            html.Tr([html.Td("Depth from ingress"), html.Td(depth_ingress_value)]),
            html.Tr([html.Td("Depth from egress"), html.Td(depth_egress_value)]),
        ])
    ], bordered=True, hover=True, responsive=True, striped=True)
