import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import seqGraph, about


'''app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Geo Map | ', href='/apps/seqGraph'),
        dcc.Link('About', href='/apps/about'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/seqGraph':
        return seqGraph.layout
    if pathname == '/apps/about':
        return about.layout
    else:
        return seqGraph.layout


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)