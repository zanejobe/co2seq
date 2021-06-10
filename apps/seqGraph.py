
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
from shapely.geometry import Point, Polygon

from app import app
from render import load_dfs, get_traces_from_dfs
import os

dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))
basins = dfs['Sedimentary Basins']
basin_names = basins.Name.unique()
basin_names.sort()


def map():
    traces = get_traces_from_dfs(dfs)

    fig = go.Figure()

    for trace in traces:
        fig.add_trace(trace)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(width=1200)
    fig.update_mapboxes(center=go.layout.mapbox.Center(lat=40, lon=-99), zoom=3)

    fig.update_layout(
        legend=dict(
            x=1,
            y=0.9,
            traceorder="normal",
            font=dict(
                family="Georgia",
                size=18,
                color="#21314D"
            )
        )
    )
    return fig

<<<<<<< HEAD
=======

'''
def boxboiz():
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

                plants_per_basin.append(plant_row['Facility Name'])
                emission_per_plant.append(plant_row['CO2 (short tons)'])

        columns = ['PlantName', 'Emissions']
        df = pd.DataFrame(columns=columns)
        df['PlantName'] = plants_per_basin
        df['Emissions'] = emission_per_plant

        basinFrames[basin_row['Name']] = df
    
    fig = px.box(basinFrames["Denver Basin"], y="Emissions", title = "graph boi")
    return fig
    '''

def scatterboiz():
    df = plants_per_basin()
    fig = px.scatter(df, x='Emissions', y='Storage', 
            title = "US Basin Sequestration Potential",
            hover_data=['Name', 'Storage', 'Emissions'])

    return fig

>>>>>>> main
def plants_per_basin():
    df_basin = dfs['Sedimentary Basins']
    df_emission = dfs['EPA Power Plants']

    exp_basin = df_basin.explode()

    co2_list = []
    storage_list = []
    names = []

    columns = ['name', 'emissions', 'storage']
    df = pd.DataFrame(columns=columns)

    for index, basin_row in exp_basin.iterrows():
        co2_mega_tons = 0.0
        
        coords = basin_row['geometry']
        poly = Polygon(coords)

        for index, plant_row in df_emission.iterrows():
            lat= plant_row["Facility Latitude"]
            lon = plant_row["Facility Longitude"]
            the_point = Point(float(lon), float(lat))

<<<<<<< HEAD
            if poly.contains(the_point) and float(plant_row["CO2 (Mt)" ]) > 0.0:
                co2_mega_tons += float(plant_row["CO2 (Mt)" ])
=======
            if poly.contains(the_point) and float(plant_row["CO2 (Mt)"]) > 0.0:
                co2_short_tons += float(plant_row["CO2 (Mt)" ])
>>>>>>> main

        if co2_mega_tons > 0.0 and basin_row['Storage'] > 0.0:
            names.append(basin_row['Name'])
            storage_list.append(basin_row['Storage'])
            co2_list.append(co2_mega_tons)
        
    df['name'] = names
    df['emissions'] = co2_list
    df['storage'] = storage_list

    return df

<<<<<<< HEAD
df = plants_per_basin()

def scatterboiz():
    fig = px.scatter(df, x='emissions', y='storage', 
            hover_data=['name', 'storage', 'emissions'], 
            log_x=True, log_y=True, 
            labels={
                "emissions" : "Emissions (Mt)",
                "storage"   : "Storage (Mt)"
            })

=======
def barboiz():
    df = plants_per_basin()
    fig = px.bar(df, x='Name', y=['Emissions','Storage'], 
            title = "Basin Sequestraion Overview"
            )
>>>>>>> main
    return fig

'''
Layout for Page 1 hosts map object and general overview
'''
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Carbon Sequestration Dashboard"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='A interactive dashboard to gain an overview of geological features relevant to the carbon sequestration process.'), className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children="Us Map of Geological Features",
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        dbc.Row([
            dcc.Graph(figure=map())
        ]),
        dbc.Row([
            dbc.Col(html.Div([
                html.H3("Basin Sequestration Potential"),
                html.H6("Scatterplot with log scale applied to x and y axis displaying all basins with their total storage and emission data."),
                dcc.Graph(figure=scatterboiz()),
            ])),
            dbc.Col(html.Div([
                html.H3("Basin Storage v. Emissions"),
                html.H6("Bar Chart per selected basin, displaying total Storage vs. Emission data."),
                dcc.Dropdown(
                    id="dropdown",
                    options=[{"label": x, "value": x} for x in basin_names],
                    value=basin_names[0],

                ),
                dcc.Graph(id="bar-graph")
            ])),
        ]),
        dbc.Row([
            dcc.Link('About', href='/apps/about')
        ])      
    ])
])
'''
Creating callback functions for bar graphs
'''
@app.callback(
    Output("bar-graph", "figure"), 
    [Input("dropdown", "value")])
def barboiz(name):
<<<<<<< HEAD
    mask = df[df["name"] == name]
    fig = px.bar(mask, x="name", y=["emissions", "storage"], 
            barmode='group',
            labels={
                "name"      : "Selected Basin",
                "emissions" : "Emissions (Mt)",
                "storage"   : "Storage (Mt)"
            })
    return fig
=======
    df = plants_per_basin()
    mask = df["Name"] == name
    fig = px.bar(df[mask], x='Name', y=['Emissions','Storage']
            )

    return fig'''



'''log 10 dataset
stacked bar chart, normalized emission type coal, gas ....
light gray backround for basins'''

>>>>>>> main
