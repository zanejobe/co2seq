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

from shapely.geometry import Point, Polygon




dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))




df_basin = dfs['Sedimentary Basins'].df
df_emission = dfs['EPA Power Plants'].df

exp_basin = df_basin.explode()


co2_list = []
storage_list = []

for index, basin_row in exp_basin.iterrows():
    co2_short_tons = 0.0
    storage_list.append(basin_row['Storage'])
    
    coords = basin_row['geometry']
    
    poly = Polygon(coords)


    for index, plant_row in df_emission.iterrows():
        lat= plant_row["Facility Latitude"]
        lon = plant_row["Facility Longitude"]
        #print(lat, lon)
        the_point = Point(float(lon), float(lat))

        if poly.contains(the_point):
            print(plant_row["CO2 (short tons)" ])

    co2_list.append(co2_short_tons)




    
    
    
