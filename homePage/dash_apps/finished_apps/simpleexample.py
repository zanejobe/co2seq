import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample')


app.layout = html.Div([
    html.H1('Square Root Slider Graph'),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(20)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
    ),
])


@app.callback(
               Output('slider-graph', 'figure'),
              [Input('slider-updatemode', 'value')])
def display_value(value):


    x = []
    for i in range(value):
        x.append(i)

    y = []
    for i in range(value):
        y.append(i*i)

    graph = go.Scatter(
        x=x,
        y=y,
        name='Manipulate Graph'
    )
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white'),

    )
    return {'data': [graph], 'layout': layout}


'''from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
from map.util import load_dfs, get_traces_from_dfs
import os

# Create your views here.

# Create your views here.
def home(request):

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
    fig.write_html("test.html")
    map_plot = plot({'data': fig}, output_type='div')
    print("done making html")

    return render(request, 'map/home.html', context={'map_plot': map_plot})'''