import shapely.geometry
import os
import plotly.graph_objects as go
import geopandas as gpd
import json
import plotly

def lat_lon_lists_from_df(df, hover_strings):
    lats = []
    lons = []
    new_hover_strings = []
    for feature, hover_string in zip(df.geometry, hover_strings):
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
                new_hover_strings.append(hover_string)
            lats.append(None)
            lons.append(None)
            new_hover_strings.append(None)
    return lats, lons, new_hover_strings

class DataFrameInfo:
    def __init__(self, lat_col, lon_col, extension, df, hover_columns):
        self.lat_col = lat_col
        self.lon_col = lon_col
        self.extension = extension
        self.df = df
        self.hover_columns = hover_columns

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
                                        # TODO: Manually specify columns from config
                                        hover_columns=df.columns[:2],
                                        df=df)
        except:
            raise Exception(f"Could not construct df from {df_file}")
    return dfs

def get_hover_string_list(df, title, hover_columns):
    result = []
    for index, row in df.iterrows():
        s = f"{title}<br>"
        for col in hover_columns:
            s += f"{col} = {row[col]}<br>"
        result.append(s)
    return result

def get_traces_from_dfs(dfs):
    traces = []
    colors = plotly.colors.qualitative.Alphabet
    counter = 1
    for df_name, df_info in dfs.items():
        df = df_info.df
        extension = df_info.extension
        hover_labels = get_hover_string_list(df, df_name, df_info.hover_columns)
        if extension == "csv":
            traces.append(go.Scattermapbox(name=df_name,
                                           visible="legendonly",
                                           hovertext=hover_labels,
                                           lat=df[df_info.lat_col], lon=df[df_info.lon_col],
                                           marker={'color': colors[counter % len(colors)], 'size': 5, 'opacity': 0.6}))
            counter += 1
        if extension == "shp" or extension == "gdb":
            if isinstance(df.geometry[0], shapely.geometry.linestring.LineString) \
                                or isinstance(df.geometry[0], shapely.geometry.multilinestring.MultiLineString):
                lats, lons, hover_labels = lat_lon_lists_from_df(df, hover_labels)
                traces.append(go.Scattermapbox(name=df_name,
                                               hovertext=hover_labels,
                                               visible="legendonly",
                                               lon=lons, lat=lats,
                                               mode='lines',
                                               line=dict(width=1, color=colors[counter % len(colors)])))
                counter += 1
            elif isinstance(df.geometry[0], shapely.geometry.point.Point):
                traces.append(go.Scattermapbox(name=df_name,
                                               hovertext=hover_labels,
                                               visible="legendonly",
                                               lat=df.geometry.y, lon=df.geometry.x,
                                               marker={'color': colors[counter % len(colors)], 'size': 5, 'opacity': 0.6}))
                counter += 1
            else:
                raise Exception(f"The geometry in {df_name} is not supported")
    return traces
