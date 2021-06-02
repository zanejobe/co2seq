
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from utils import *
import os



def graphing(dataframes):

    dfs = dataframes
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


# ------------------------------------------------------------------------------
# App layout
app = dash.Dash(__name__)
#define interface

#dataframes of all data
dfs = load_dfs(os.path.join("Data", "lightweight_config.json"))
df = dfs.get('EPA Power Plants')

available_indicators = dfs.keys()
print(available_indicators)



app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
    ]),

    html.Div([
        dcc.Graph(figure=graphing(dfs))
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
