import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import geopandas as gpd
import pandas as pd

import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash
from dash.dependencies import Output, Input
from dash_extensions.javascript import arrow_function

from app import app
from utils import *
import os

from shapely.geometry import Point, Polygon

dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))
basins = dfs['Sedimentary Basins'].df
basin_names = basins.Name.unique()


def plants_per_basin():
    df_basin = dfs['Sedimentary Basins'].df
    df_emission = dfs['EPA Power Plants'].df

    exp_basin = df_basin.explode()

    co2_list = []
    storage_list = []
    names = []

    columns = ['name', 'emissions', 'storage']
    df = pd.DataFrame(columns=columns)

    for index, basin_row in exp_basin.iterrows():
        co2_short_tons = 0.0
        
        coords = basin_row['geometry']
        poly = Polygon(coords)

        for index, plant_row in df_emission.iterrows():
            lat= plant_row["Facility Latitude"]
            lon = plant_row["Facility Longitude"]
            the_point = Point(float(lon), float(lat))

            if poly.contains(the_point) and float(plant_row["CO2 (short tons)" ]) > 0.0:
                co2_short_tons += float(plant_row["CO2 (short tons)" ])

        if co2_short_tons > 0.0 and basin_row['Storage'] > 0.0:
            names.append(str(basin_row['Name']))
            storage_list.append(float(basin_row['Storage']))
            co2_list.append(co2_short_tons)
        
    df['name'] = names
    df['emissions'] = co2_list
    df['storage'] = storage_list

    return df
'''def barboiz():
    df = plants_per_basin()
    #mask = df["name"] == name
    #df = plants_per_basin()
    fig = px.bar(df["Denver Basin"], x="name", y="emissions",
            barmode="group")

    return fig

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in basin_names],
        value=basin_names[0],
        clearable=False,
    ),
    dcc.Graph(id="bar-graph",
            figure=barboiz())
])'''

'''@app.callback(
    Output("bar-graph", "figure"), 
    [Input("dropdown", "value")])'''
'''def barboiz():
    df = plants_per_basin()
    #mask = df["name"] == name
    #df = plants_per_basin()
    fig = px.bar(df["Denver Basin"], x="names", y="emissions",
            barmode="group")

    return fig

app.run_server(debug=True)'''



print(plants_per_basin()["name"] == 'Denver Basin')