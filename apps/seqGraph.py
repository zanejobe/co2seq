import plotly.graph_objects as go
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

import dash
from dash.dependencies import Output, Input

from app import app
from render import load_dfs, get_traces_from_dfs
import os

dfs = load_dfs(os.path.join("Data", "config.json"))
traces = get_traces_from_dfs(os.path.join("Data", "config.json"), dfs)
basins = dfs['USGS Sedimentary Basins 2012']

fig = go.Figure()

for trace in traces:
    fig.add_trace(trace)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

map_height = 600
fig.update_layout(height=map_height)
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


df = pd.read_csv("Data/plants_per_basin.csv")
basin_names = df.name.unique()
basin_names.sort()

def scatterboiz():
    df["Years to fill basin"] = (df.apply(lambda x: round(x.storage/x.emissions, 2), axis=1))
    fig = px.scatter(df, x='emissions', y='storage',
            hover_data=['name', 'storage', 'emissions', 'Years to fill basin'],
            size='Years to fill basin',
            log_x=True, log_y=True, 
            labels={
                "emissions" : "2020 Emissions (Mt)",
                "storage"   : "Total Storage Potential (Mt)"
            })
    fig.update_layout(yaxis={"tickmode": "linear", "showgrid": False},
                      xaxis={"tickmode": "linear", "showgrid": False})
    return fig

'''
Layout for Page 1 hosts map object and general overview
'''
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Dashboard for Carbon Capture, Utilization, and Storage (CCUS) Data"), className="mb-2"),
            dbc.Col(dcc.Link('About', href='/apps/about', style={"textAlign": "right"}), style={"textAlign": "right"})
        ], style={"margin-top": "6px"}),
        dbc.Row([
            dbc.Col(html.H6(children='Colorado School of Mines'))
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='An interactive dashboard to visualize geospatial data relevant to CCUS efforts in the United States. Select a dataset below to visualize it on the map, or scroll down to explore CCUS statistics grouped by basin.'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(html.H3("CCUS Map (select a dataset on the right to visualize it)", className="align-self-center"))
                     
                ], color="rgb(33,49,77,0.9)", inverse=True)),
            ], style={
                'textAlign': 'center',
            }),
        dbc.Row([
            dcc.Loading(
                id="loading-1",
                type="default",
                style={"height": f"{map_height}", "width": "175vh"},
                children=dcc.Graph(id="map", style={"height": f"{map_height}", "width": "175vh"})
            ),
        ], id="map_row", justify="center"),
        dbc.Row(children=
            [
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("CCUS Potential for US Basins", className="card-title"), 
                        html.P("Each dot represents a US basin, where the annual emissions are derived from EPA data and the total carbon storage is derived from USGS data", className="card-text"),
                        html.P("Bubble size represents the number of years of emissions to fill the storage")])
                ], color="rgb(210,73,42,0.9)", inverse=True)),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Select a basin to compare emissions and storage", className="card-title"), 
                        html.P("Bar chart compares annual emissions and total storage for a particular basin", className="card-text")]),
                    dbc.CardFooter(
                        dcc.Dropdown(
                            id="dropdown",
                            options=[{"label": x, "value": x} for x in basin_names],
                            value=basin_names[0],
                            style={'color': 'black'}
                        ),
                    ),
                ], color="rgb(210,73,42,0.9)", inverse=True))
            ], style={
                'textAlign': 'center', 'margin-top': '10px'
            }), 
        dbc.Row(children=
            [
                dbc.Col(html.Div([
                    dcc.Graph(figure=scatterboiz(), responsive=True),
                ])),
                dbc.Col(html.Div([
                    dcc.Graph(id="bar-graph", responsive=True),
                ]))
            ])
    ], fluid=True)
])
'''
Creating callback functions for bar graphs
'''
@app.callback(
    [Output("bar-graph", "figure"), Output("dropdown", "value")],
    [Input("dropdown", "value"), Input("map", "clickData")])
def barboiz(name, clickData):
    ctx = dash.callback_context
    changed = ctx.triggered[0]['prop_id'].split('.')[0]

    # If a user clicks on the map, parse the clickData from dcc.Graph into a name
    if changed == "map" and clickData:
        for frame in dfs.values():
            row = frame[frame["hover"] == clickData["points"][0]["hovertext"]]
            if not row.empty:
                name = row["Name"].values[0]

    mask = df[df["name"] == name]
    fig = px.bar(mask, x="name", y=["emissions", "storage"], barmode='group', log_y=True)
    fig.update_layout(yaxis={"tickmode": "linear", "showgrid": False, "title": "CO<sub>2</sub> (Mt)" },
                      xaxis={"title": ""})
    return fig, name

@app.callback(
    Output("map", "figure"),
    [Input("map_row", "id")])
def create_map(_):
    return fig
