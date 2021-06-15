


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


from app import app


layout = html.Div([
    dbc.Container([
        dbc.Row([
            html.H1("About Page"), 
        ]),
        dbc.Row([
            html.H3("Project Overview"),
            html.H6("This project is an interactive dashboard that uses public datasets relevant fo a co2 sink and source information from various agencies for users to explore. The data is contained in the Data folder and described in config.json. Each dataset is imposed on a map of the US and Gulf of Mexico that the user is able to explore and view summary information for. Links to all data sources can be found below. The project is a built as a Dash app by Plotly, and uses the associated libraries to represent the data. All graphing is handeled in apps/seqGraph.py. And data is processed in utils.py and render.py."),
        ]),
        dbc.Row([
            dcc.Markdown('''
                ## Desinged by Colorado School of Mines  
                Team Lead: Professor Zane Jobe zanejobe@mines.edu  
                Contributers: Grant Falkner, Matt Plumb, Ryan Armstrong, Patrick Schassberger  
                '''
            )
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
        dbc.Row([
            html.H6("Last update: 05/15/2021"),
        ]),
        html.Br(),
        dcc.Link('Home', href='/'),
    ])
])