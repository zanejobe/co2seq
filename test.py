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

from dash import Dash
from dash.dependencies import Output, Input
from dash_extensions.javascript import arrow_function

from app import app
from utils import *
import os

from shapely.geometry import Point, Polygon

dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))

df_basin = dfs['Sedimentary Basins'].df
df_emission = dfs['EPA Power Plants'].df

exp_basin = df_basin.explode()   

basinFrames = {}

for index, basin_row in exp_basin.iterrows():
    plants_per_basin = []
    emission_per_plant = []
    
    coords = basin_row['geometry']
    poly = Polygon(coords)

    for index, plant_row in df_emission.iterrows():
        lat= plant_row["Facility Latitude"]
        lon = plant_row["Facility Longitude"]
        the_point = Point(float(lon), float(lat))

        if poly.contains(the_point) and float(plant_row["CO2 (short tons)" ]) > 0.0:

            print(plant_row)

            plants_per_basin.append(plant_row["Facility Name"])
            emission_per_plant.append(plant_row['CO2 (short tons)'])

    columns = ['PlantName', 'Emissions']
    df = pd.DataFrame(columns=columns)
    df['PlantName'] = plants_per_basin
    df['Emissions'] = emission_per_plant

    basinFrames[basin_row['Name']] = df

fig = px.box(basinFrames.keys()[0], y="Emissions", title = "graph boi")

fig.show()


    
    
    
