import plotly.graph_objects as go
from plotly.offline import plot

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import geopandas as gpd

from app import app
from utils import *
import os

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("About"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Data sources and relevant links.'), className="mb-4")
        ]),
    ])
])