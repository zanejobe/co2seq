
'''import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import geopandas as gpd

from utils import *
import os


# ------------------------------------------------------------------------------
# App layout
app = dash.Dash(__name__)
#define interface

#dataframes of all data
dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))
df = dfs.get('EPA Power Plants')

data = gpd.read_file("Data/platform.zip")
data2 = gpd.read_file("Data/PowerPlants_US_EIA.zip")

data_dict = {
    "Platform"  : data,
    "Plants"    : data2
}

available_indicators = data_dict.keys()
#print(available_indicators)


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='selected-plot',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Platform',
                multi=True,
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
    ]),

    html.Div([
        dcc.Graph(id='northAmericaMap')
    ])
])

@app.callback(
    Output('northAmericaMap', 'figure'),
    Input('selected-plot', 'value'))
def update_figure(selected_plot):
    print(selected_plot)
   
    filtered_df = data_dict.get(selected_plot)

    fig = px.scatter_mapbox(filtered_df, lat=filtered_df['geometry'].y, lon=filtered_df['geometry'].x)

    fig.update_layout(mapbox_style="open-street-map", transition_duration=500)

    return fig




import plotly.graph_objects as go
from plotly.offline import plot

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import geopandas as gpd


from utils import *
import os

def theMap():

    dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))
    traces = get_traces_from_dfs(dfs)

    fig = go.Figure()

    for trace in traces:
        fig.add_trace(trace)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(autosize=True)
    fig.update_layout(title={"text": "Carbon Sequestration Dashboard",
        "font": {"family": "Helvetica", "size": 28, "color": "#263F6A"}, "x": 0.01, "y": 0.98})
    fig.update_mapboxes(center=go.layout.mapbox.Center(lat=40, lon=-99), zoom=3)

    fig.update_layout(
        legend=dict(
            x=1,
            y=0.97,
            traceorder="normal",
            font=dict(
                family="Georgia",
                size=18,
                color="#21314D"
            )
        )
    )

    return fig

# App layout
app = dash.Dash(__name__)
'''
'''
Layout for Page 1 hosts map object and general overview
'''
'''
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Carbon Sequestration Dashboard"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='A interactive dashboard to gain an overview of geological features relevant to the carbon sequestration process.'), className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Map',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),

    dcc.RadioItems(
        id='table_type',
        options=[{'label': i, 'value': i} for i in ['About']],
        value='Condensed table',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(
        id='northAmericanMap',
        figure=theMap()
    ),
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)'''


import dash

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
