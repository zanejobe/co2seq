import plotly.graph_objects as go
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

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
    fig = px.scatter(df, x='emissions', y='storage', 
            hover_data=['name', 'storage', 'emissions'], 
            log_x=True, log_y=True, 
            labels={
                "emissions" : "Emissions (Mt)",
                "storage"   : "Storage (Mt)"
            })
    fig.update_layout(yaxis={"tickmode": "linear"},
                      xaxis={"tickmode": "linear"})
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
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(html.H3("US Map of Sequestration Features", className="align-self-center"))
                     
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
                        html.H4("Basin Sequestration Potential", className="card-title"), 
                        html.P("Scatterplot with log scale applied to x and y axis displaying all basins with their total storage and emission data.", className="card-text")]),
                ], color="rgb(210,73,42,0.9)", inverse=True)),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Basin Storage v. Emissions", className="card-title"), 
                        html.P("Bar Chart per selected basin, displaying total Storage vs. Emission data.", className="card-text")]),
                    dbc.CardFooter(
                        dcc.Dropdown(
                            id="dropdown",
                            options=[{"label": x, "value": x} for x in basin_names],
                            value=basin_names[0],
                            style={'color': 'black'}
                        ) 
                    ),
                ], color="rgb(210,73,42,0.9)", inverse=True))
            ], style={
                'textAlign': 'center',
            }), 
        dbc.Row(children=
            [
                dbc.Col(html.Div([
                    dcc.Graph(figure=scatterboiz()),
                ])),
                dbc.Col(html.Div([
                    dcc.Graph(id="bar-graph"),
                ]))
            ]), 
        dbc.Row([
            dbc.Card([
                dbc.CardBody([
                    dcc.Link('About', href='/apps/about')
                ])
            ])
            
        ], style={
                'textAlign': 'right',
            })   
    ], fluid=True)
])
'''
Creating callback functions for bar graphs
'''
@app.callback(
    Output("bar-graph", "figure"), 
    [Input("dropdown", "value")])
def barboiz(name):
    mask = df[df["name"] == name]
    fig = px.bar(mask, x="name", y=["emissions", "storage"], barmode='group', log_y=True)
    fig.update_layout(yaxis={"tickmode": "linear"})
    return fig

@app.callback(
    Output("map", "figure"),
    [Input("map_row", "id")])
def create_map(_):
    return fig
