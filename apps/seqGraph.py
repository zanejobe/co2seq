
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import geopandas as gpd
import json

from app import app
from utils import *
import os


def theMap():

    dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))
    traces = get_traces_from_dfs(dfs)

    fig = go.Figure()

    for trace in traces:
        fig.add_trace(trace)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(autosize=True)
    fig.update_mapboxes(center=go.layout.mapbox.Center(lat=40, lon=-99), zoom=3)

    fig.update_layout(
        legend=dict(
            x=1,
            y=0.9,
            traceorder="normal",
            font=dict(
                family="Georgia",
                size=18,
                color="#21314D"
            )
        )
    )

    return fig
def lineboiz():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title = "graph boi")
    return fig

def barboiz():
    df = px.data.tips()
    fig = px.box(df, y="total_bill", title = "graph boi")
    return fig
'''
Layout for Page 1 hosts map object and general overview
'''
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Carbon Sequestration Dashboard"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='A interactive dashboard to gain an overview of geological features relevant to the carbon sequestration process.'), className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Map',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        dbc.Row([
            html.Div([
                dl.Map(
                children=[
                    dl.TileLayer(),
                    dl.GeoJSON(url="assets/basins.geojson", id="capitals"),
                    dl.GeoJSON(url="assets/pipelines.geojson", id="pipelines"),
                    # dl.GeoJSON(data=power_plants, id="powerplants")

                ],
                zoom=5,
                style={'width': '600px',
                      'height': '500px',
                      'padding': '5px',
                      'display': 'table-cell'}),
                ]),
        ]),
        dbc.Row([
            dbc.Col(html.Div(
                dcc.Graph(figure=barboiz())
            )),
            dbc.Col(html.Div(
                dcc.Graph(figure=lineboiz())
            )),
        ]),
        dbc.Row([
            dcc.Link('About', href='/apps/about')
        ])      
    ])
])
'''
Callback to make datapoints interactive
'''

'''@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open'''