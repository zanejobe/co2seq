
import pandas as pd
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
'''dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))
df = dfs.get('EPA Power Plants')'''

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

if __name__ == '__main__':
    app.run_server(debug=True)



