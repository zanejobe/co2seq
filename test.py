import dash
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import json

import geopandas as gpd
from utils import *


dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))

for df in dfs.values():
    geo = df.df
    geo.to_file("GeoDataMap.geojson", driver='GeoJSON')
