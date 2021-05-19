from django.shortcuts import render
from django.http import HttpResponse

import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
import pandas as pd
import geopandas as gpd

'''https://medium.com/analytics-vidhya/plotly-for-geomaps-bb75d1de189f
https://plotly.com/python/map-configuration/
https://plotly.com/python/bubble-maps/#bubble-map-with-goscattergeo'''

# Create your views here.
def NorthAmericaView(request):
    '''df = px.data.gapminder().query("year==2007")
    fig = px.scatter_geo(df, locations="iso_alpha", color="continent",
                        hover_name="country", size="pop",
                        projection="natural earth")'''


    '''fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        resolution=50,
        showcoastlines=True, coastlinecolor="RebeccaPurple", scope="north america",
        showland=True, landcolor="LightGreen",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="Blue",
        showrivers=True, rivercolor="Blue"
    )
    fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
    map_plot = plot({'data': fig}, output_type='div')'''

    # add two dataframes
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
    print(us_cities.head())
    platforms = gpd.read_file("files/platform.zip")

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

    map_plot = plot({'data': fig}, output_type='div')

    return render(request, 'northAmericanMap.html', context={'map_plot': map_plot})


us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
#print(us_cities.head())
platforms = gpd.read_file("files/platform.zip")

temp = pd.DataFrame()

temp['lon'] = platforms['geometry'].x
temp['lat'] = platforms['geometry'].y

platforms['lat'] = temp['lat']
platforms['lon'] = temp['lon']

data_dict = {"cities": us_cities, "platforms": platforms}

print(data_dict['platforms']['lon'])