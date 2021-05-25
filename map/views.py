from django.shortcuts import render
#from django.http import HttpResponse
#used imports
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
import pandas as pd
import geopandas as gpd

# Create your views here.

'''def home(request):
    return render(request, 'map/home.html')'''


def about(request):
    return render(request, 'map/about.html')

# Create your views here.
def home(request):
    # add two dataframes
    platforms = gpd.read_file("Data/platforms/platform.zip")
    plantsEmissions = gpd.read_file("Data/EPAEmissions/emission_05-24-2021.csv")


    '''
    Some datasets needed us to split the geometry data
    '''
    temp = pd.DataFrame()
    temp['lon'] = platforms['geometry'].x
    temp['lat'] = platforms['geometry'].y
    platforms['lat'] = temp['lat']
    platforms['lon'] = temp['lon']


    # create figure object
    fig = go.Figure()
    # add traces to figure object
    fig.add_trace(go.Scattermapbox(lat=plantsEmissions['Facility Latitude'], lon=plantsEmissions['Facility Longitude'], 
                    name='Plants', visible='legendonly'))

    fig.add_trace(go.Scattermapbox(lat=platforms['lat'], lon=platforms['lon'], 
                    name='Platforms', visible='legendonly'))
            
    
    # define layout
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

    return render(request, 'map/home.html', context={'map_plot': map_plot})