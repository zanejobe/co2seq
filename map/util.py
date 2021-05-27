import shapely.geometry
import os
import plotly.graph_objects as go
import geopandas as gpd
import json
import plotly

def lat_lon_lists_from_df(df):
    lats = []
    lons = []
    for feature in df.geometry:
        if isinstance(feature, shapely.geometry.linestring.LineString):
            linestrings = [feature]
        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
            linestrings = feature.geoms
        else:
            continue
        for linestring in linestrings:
            x, y = linestring.xy
            for lat, lon in zip(y, x):
                lats.append(lat)
                lons.append(lon)
            lats.append(None)
            lons.append(None)
    return lats, lons

class DataFrameInfo:
    def __init__(self, lat_col, lon_col, extension, df):
        self.lat_col = lat_col
        self.lon_col = lon_col
        self.extension = extension
        self.df = df

def load_dfs(config_path, data_dir="Data"):
    dfs = {}
    f = open(config_path)
    config = json.load(f)
    for config_df in config['dataframes']:
        df_key = config_df["name"]
        df_file = os.path.join(data_dir, config_df["file"])
        try:
            df = gpd.read_file(df_file)
            dfs[df_key] = DataFrameInfo(lat_col=config_df["latcol"],
                                        lon_col=config_df["loncol"],
                                        extension=config_df["file_type"],
                                        df=df)
        except:
            raise Exception(f"Could not construct df from {df_file}")
    return dfs

def get_traces_from_dfs(dfs):
    traces = []
    colors = plotly.colors.qualitative.Alphabet
    counter = 1
    for df_name, df_info in dfs.items():
        df = df_info.df
        extension = df_info.extension
        if extension == "csv":
            traces.append(go.Scattermapbox(name=df_name,
                                           visible="legendonly",
                                           lat=df[df_info.lat_col], lon=df[df_info.lon_col],
                                           marker={'color': colors[counter % len(colors)], 'size': 5, 'opacity': 0.6}))
            counter += 1
        if extension == "shp" or extension == "gdb":
            if isinstance(df.geometry[0], shapely.geometry.linestring.LineString) \
                                or isinstance(df.geometry[0], shapely.geometry.multilinestring.MultiLineString):
                lats, lons = lat_lon_lists_from_df(df)
                traces.append(go.Scattermapbox(name=df_name,
                                               visible="legendonly",
                                               lon=lons, lat=lats,
                                               mode='lines',
                                               line=dict(width=1, color=colors[counter % len(colors)])))
                counter += 1
            elif isinstance(df.geometry[0], shapely.geometry.point.Point):
                traces.append(go.Scattermapbox(name=df_name,
                                               visible="legendonly",
                                               lat=df.geometry.y, lon=df.geometry.x,
                                               marker={'color': colors[counter % len(colors)], 'size': 5, 'opacity': 0.6}))
                counter += 1
            else:
                raise Exception(f"The geometry in {df_name} is not supported")
    return traces
