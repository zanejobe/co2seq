


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
            html.H6("This project is an interactive dashboard that uses public datasets relevant to CO2 sink and source information. Each dataset is imposed on a map of the U.S. that the user is able to explore and view summary information for. Links to all data sources can be found below."),
        ]),
        dbc.Row([
            html.H6("Designed by faculty and students at the Colorado School of Mines as part of a computer science field session project"),

        ]),
        dbc.Row([
            html.H6("Team Lead: Professor Zane Jobe zanejobe@mines.edu"),

        ]),
        dbc.Row([
            html.H6("Contributors: Grant Falkner, Matt Plumb, Ryan Armstrong, Patrick Schassberger")
        ]),
        dbc.Row([
            html.H3("Notes Regarding Data")
        ]),
        dbc.Row([
            dcc.Markdown('''
            - All numeric axes are logarithmicly scaled for readability
            - The study areas taken from the USGS basin storage data and actual geological basins do not entirely line up. As a result, some basins do not have storage data and are excluded from the two graphs. Storage values also may not be entirely accurate due to the difference in area.
            
            ''')
        ]),
        dbc.Row([
            html.H3("References")
        ]),
        dbc.Row([
            dcc.Markdown(
        '''
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
            html.H6("Last update: 06/16/2021"),
        ]),
        html.Br(),
        dcc.Link('Home', href='/'),
    ])
])