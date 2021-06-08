
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import geopandas as gpd

import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash
from dash.dependencies import Output, Input
from dash_extensions.javascript import arrow_function

from app import app
from utils import *
import os




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

def lineboiz():
    df_basin = dfs['Sedimentary Basins'].df
    df_emission = dfs['EPA Power Plants'].df

    for basin in df_basin.value():
        

    fig = px.scatter(df, x="year", y="lifeExp", title = "graph boi")
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
            dcc.Graph(
                id='northAmericanMap',
                figure=fig,
            )
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
