


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


from app import app


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("About"), className="mb-2")
        ]),
        dbc.Row([
            dcc.Markdown(
        '''
        
## References
Every dataset used contains non-proprietary data from U.S. government agencies:

- USGS Sedimentary Basins - https://pubs.usgs.gov/of/2012/1111/
- USGS Basin Storage 2012 - https://pubs.usgs.gov/ds/774/
- EPA Power Plants 2020 - https://ampd.epa.gov/ampd/
- EIA Pipelines and Powerplants - https://www.eia.gov/maps/layer_info-m.php
- BOEM Boreholes 2021 - https://www.data.boem.gov/Main/Well.aspx
- BOEM GOM Sands 2019 - https://www.data.boem.gov/Main/GandG.aspx
- BOEM Planned Wells 2021 - https://www.data.boem.gov/Main/Plans.aspx
- BOEM Pipelines and Platforms 2021 - https://www.data.boem.gov/Main/Mapping.aspx
- NETL GOM Wells 2019 - https://edx.netl.doe.gov/geocube/#collections/offshore
- USGS Seismic Data (NAMSS) 2016 - https://walrus.wr.usgs.gov/namss/search/

        '''
            )
        ]),
        html.Br(),
        dcc.Link('Home', href='/'),
    ])
])