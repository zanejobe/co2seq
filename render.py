import json
import os
import plotly.graph_objects as go
from utils import *

plotly_args = {
    "point": {"mode": "markers", "fill": "none"},
    "line": {"mode": "lines", "fill": "none"},
    "polygon": {"mode": "lines", "fill": "toself"}
}


def load_dfs(config_path, data_dir="Data"):
    '''
        Load all files in config into GeoPandas dataframes

        Args:
            config_path::str
                Path to the data configuration JSON file
            data_dir::str
                Path to the directory containing the Data files referenced by the config

        Returns:
            {name:dfs}::{str:geopandas.GeoDataFrame}
                Returns a dictionary of dataframes
    '''
    dfs = {}
    try:
        f = open(config_path)
        config = json.load(f)
    except:
        raise Exception(f"Error loading config file from {config_path}")

    for conf in config['dataframes']:
        df_file = os.path.join(data_dir, conf["file"])
        try:
            df = gpd.read_file(df_file)

            if conf["file_type"] == "csv":
                df = clean_csv_df(df, conf["latcol"], conf["loncol"])

            df["hover"] = get_hover_string_list(df, conf["attributes_to_display"])
            dfs[conf["name"]] = df
        except:
            raise Exception(f"Could not construct df from {df_file}")
    return dfs


def get_traces_from_dfs(config_path, dfs):
    '''
        Turn a dictionary of dataframes into a list of ScatterMapBox traces
        to be added to a plotly figure

        Args:
            {name:dfs}::{str:geopandas.GeoDataFrame}
                A dictionary of GeoPandas dataframes created from load_dfs()
            config_path::str
                Path to the data configuration JSON file

        Returns:
            traces::[plotly.graph_objects.Scattermapbox]
    '''
    traces = []
    try:
        f = open(config_path)
        config = json.load(f)
    except:
        raise Exception(f"Error loading config file from {config_path}")

    for conf in config["dataframes"]:
        name = conf["name"]
        df = dfs[name]

        key = get_shapley_key(df.geometry[0])
        if key == "":
            raise Exception(f"The geometry in {name} is not supported")

        lats, lons, hover_labels = lat_lon_lists_from_df(df)
        # TODO: specify line thicknesses, point sizes, and colors

        if name == "Sedimentary Basins":
            traces.append(go.Scattermapbox(name=name,
                                       hovertext=hover_labels,
                                       visible="legendonly",
                                       lon=lons, lat=lats,
                                       marker=dict(color='rgba(172,177,180, 0.6)'),
                                       mode=plotly_args[key]["mode"],
                                       fill=plotly_args[key]["fill"]))

        else:
            traces.append(go.Scattermapbox(name=name,
                                        hovertext=hover_labels,
                                        visible="legendonly",
                                        lon=lons, lat=lats,
                                        mode=plotly_args[key]["mode"],
                                        fill=plotly_args[key]["fill"]))
    return traces


def lat_lon_lists_from_df(df):
    '''
        Converts a GeoPandas dataframe's geometry into plottable lists of lat, lon, and hover_strings
        to be used by plotly

        Args:
            df::geopandas.GeoDataFrame
                A GeoPandas Dataframe containing "geometry" and "hover" columns

        Returns:
            (lats, lons, hover_strings)::([float], [float], [str])
                Three lists which reference a list of latitude values, longitude values,
                and hover strings respectively
    '''
    lats = []
    lons = []
    hover_strings = []
    for feature, hover_string in zip(df["geometry"], df["hover"]):
        if is_shapley_multi(feature):
            shapes = feature.geoms
        else:
            shapes = [feature]
        for shape in shapes:
            if is_shapley_line(shape):
                x, y = shape.xy
            elif is_shapley_polygon(shape):
                x, y = shape.exterior.coords.xy
            elif is_shapley_point(shape):
                lats.append(shape.y)
                lons.append(shape.x)
                hover_strings.append(hover_string)
                continue
            for lat, lon in zip(y, x):
                lats.append(lat)
                lons.append(lon)
                hover_strings.append(hover_string)
            lats.append(None)
            lons.append(None)
            hover_strings.append(None)
    return lats, lons, hover_strings
