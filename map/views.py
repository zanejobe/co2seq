from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
from map.util import load_dfs, get_traces_from_dfs
import os

# Create your views here.

'''def home(request):
    return render(request, 'map/home.html')'''


def about(request):
    return render(request, 'map/about.html')

# Create your views here.
def home(request):

    dfs = load_dfs(os.path.join("Data", "config.json"))
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

    map_plot = plot({'data': fig}, output_type='div')

    return render(request, 'map/home.html', context={'map_plot': map_plot})
