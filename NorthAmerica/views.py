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
    # add two dataframes
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
    platforms = gpd.read_file("files/platform.zip")

    temp = pd.DataFrame()

    temp['lon'] = platforms['geometry'].x
    temp['lat'] = platforms['geometry'].y

    platforms['lat'] = temp['lat']
    platforms['lon'] = temp['lon']

    #build dictionary of df's
    data_dict = {"cities": us_cities, "platforms": platforms}

    print(platforms.head())
    print(us_cities.head())

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(lat=us_cities['lat'], lon=us_cities['lon'], 
                    name='Cities', hoverinfo=us_cities['Cities']))

    fig.add_trace(go.Scattermapbox(lat=platforms['lat'], lon=platforms['lon'], 
                    name='Oil Rigs'))
    
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_mapboxes(center=go.layout.mapbox.Center(lat=40, lon=-99), zoom=3)

    fig.update_layout(
        legend=dict(
            x=1,
            y=1,
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=20,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        )
    )

    map_plot = plot({'data': fig}, output_type='div')

    return render(request, 'northAmericanMap.html', context={'map_plot': map_plot})
