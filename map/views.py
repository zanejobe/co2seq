from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
from map.util import load_dfs, get_traces_from_dfs
import os
import geopandas as gpd

# Create your views here.

'''def home(request):
    return render(request, 'map/home.html')'''


def about(request):
    return render(request, 'map/about.html')

# Create your views here.
def home(request):

    us_cities = gpd.read_file("Data/PowerPlants_US_EIA.zip")
    platforms = gpd.read_file("Data/platform.zip")
    temp = pd.DataFrame()
    temp['lon'] = platforms['geometry'].x
    temp['lat'] = platforms['geometry'].y
    platforms['lat'] = temp['lat']
    platforms['lon'] = temp['lon']
    #build dictionary of df's
    data_dict = {"cities": us_cities, "platforms": platforms}
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(lat=us_cities['lat'], lon=us_cities['lon']))
    fig.add_trace(go.Scattermapbox(lat=platforms['lat'], lon=platforms['lon']))
    

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_mapboxes(center=go.layout.mapbox.Center(lat=40, lon=-99), zoom=3)

    map_plot = plot({'data': fig}, output_type='div')

    return render(request, 'map/home.html', context={'map_plot': map_plot})


