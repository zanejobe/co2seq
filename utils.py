import shapely.geometry
import os
import plotly.graph_objects as go
import geopandas as gpd
import json
import plotly


def lat_lon_lists_from_df(df, hover_strings):
    '''
        Converts a dataframe's geometry into plottable lists of lat, lon, and hover_strings
        to be used by plotly
    '''
    lats = []
    lons = []
    new_hover_strings = []
    for feature, hover_string in zip(df.geometry, hover_strings):
        if isinstance(feature, shapely.geometry.linestring.LineString)\
                or isinstance(feature, shapely.geometry.polygon.Polygon):
            linestrings = [feature]
        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString)\
                or isinstance(feature, shapely.geometry.multipolygon.MultiPolygon):
            linestrings = feature.geoms
        else:
            continue
        for linestring in linestrings:
            x = []
            y = []
            if isinstance(linestring, shapely.geometry.linestring.LineString):
                x, y = linestring.xy
            if isinstance(linestring, shapely.geometry.polygon.Polygon):
                x, y = linestring.exterior.coords.xy
            for lat, lon in zip(y, x):
                lats.append(lat)
                lons.append(lon)
                new_hover_strings.append(hover_string)
            lats.append(None)
            lons.append(None)
            new_hover_strings.append(None)
    return lats, lons, new_hover_strings

def load_dfs(config_path, data_dir="Data"):
    '''
        Load all files in config into GeoPandas dataframes
    '''
    dfs = {}
    f = open(config_path)
    config = json.load(f)
    for conf in config['dataframes']:
        df_file = os.path.join(data_dir, conf["file"])
        try:
            df = gpd.read_file(df_file)

            if conf["file_type"] == "csv":
                df = df[df[conf["latcol"]] != ""]
                df = df[df[conf["loncol"]] != ""]
                df.geometry = gpd.points_from_xy(df[conf["latcol"]], df[conf["loncol"]])

            df["hover"] = get_hover_string_list(df, conf["attributes_to_display"])
            dfs[conf["name"]] = df
        except:
            raise Exception(f"Could not construct df from {df_file}")
    return dfs

def get_hover_string_list(df, hover_columns):
    result = []
    for index, row in df.iterrows():
        s = ""
        for col in hover_columns:
            if col in row:
                s += f"{col} = {row[col]}<br>"
        result.append(s)
    return result

def get_traces_from_dfs(dfs):
    traces = []
    colors = plotly.colors.qualitative.Dark24
    counter = 1
    for name, df in dfs.items():
        if isinstance(df.geometry[0], shapely.geometry.linestring.LineString) \
                            or isinstance(df.geometry[0], shapely.geometry.multilinestring.MultiLineString):
            lats, lons, hover_labels = lat_lon_lists_from_df(df, df["hover"])
            traces.append(go.Scattermapbox(name=name,
                                           hovertext=hover_labels,
                                           visible="legendonly",
                                           lon=lons, lat=lats,
                                           mode='lines',
                                           line=dict(width=1, color=colors[counter % len(colors)])))
            counter += 1
        elif isinstance(df.geometry[0], shapely.geometry.point.Point):
            traces.append(go.Scattermapbox(name=name,
                                           hovertext=df["hover"],
                                           visible="legendonly",
                                           lat=df.geometry.y, lon=df.geometry.x,
                                           marker={'color': colors[counter % len(colors)], 'size': 5, 'opacity': 0.6}))
            counter += 1
        elif isinstance(df.geometry[0], shapely.geometry.polygon.Polygon):
            lats, lons, hover_labels = lat_lon_lists_from_df(df, df["hover"])
            traces.append(go.Scattermapbox(name=name,
                                           hovertext=hover_labels,
                                           visible="legendonly",
                                           fill="toself",
                                           lon=lons, lat=lats,
                                           mode='lines',
                                           line=dict(width=1, color=colors[counter % len(colors)])))
            counter += 1
        else:
            raise Exception(f"The geometry in {name} is not supported")
    return traces