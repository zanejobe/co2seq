from django.shortcuts import render
from django.http import HttpResponse

import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px

'''https://medium.com/analytics-vidhya/plotly-for-geomaps-bb75d1de189f
https://plotly.com/python/map-configuration/
https://plotly.com/python/bubble-maps/#bubble-map-with-goscattergeo'''

# Create your views here.
def NorthAmericaView(request):
    df = px.data.gapminder().query("year==2007")
    fig = px.scatter_geo(df, locations="iso_alpha", color="continent",
                        hover_name="country", size="pop",
                        projection="natural earth")


    '''fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        resolution=100,
        showcoastlines=True, coastlinecolor="RebeccaPurple", scope="north america",
        showland=True, landcolor="LightGreen",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="Blue",
        showrivers=True, rivercolor="Blue"
    )'''
    fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
    map_plot = plot({'data': fig}, output_type='div')

    return render(request, 'northAmericanMap.html', context={'map_plot': map_plot})
