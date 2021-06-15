import shapely.geometry
import geopandas as gpd

def is_shapley_point(geom):
    return isinstance(geom, shapely.geometry.point.Point) \
           or isinstance(geom, shapely.geometry.multipoint.MultiPoint)


def is_shapley_polygon(geom):
    return isinstance(geom, shapely.geometry.polygon.Polygon) \
           or isinstance(geom, shapely.geometry.multipolygon.MultiPolygon)


def is_shapley_line(geom):
    return isinstance(geom, shapely.geometry.linestring.LineString) \
           or isinstance(geom, shapely.geometry.multilinestring.MultiLineString)


def is_shapley_multi(geom):
    return isinstance(geom, shapely.geometry.multipolygon.MultiPolygon) \
           or isinstance(geom, shapely.geometry.multipoint.MultiPoint) \
           or isinstance(geom, shapely.geometry.multilinestring.MultiLineString)


def get_shapley_key(geom):
    if is_shapley_point(geom):
        return "point"
    elif is_shapley_line(geom):
        return "line"
    elif is_shapley_polygon(geom):
        return "polygon"
    return ""

def clean_csv_df(df, lat_col, lon_col):
    '''
        Clean up a dataframe created from a csv file. This involves
        - Stripping any rows where the lat/lon evaluate to false (empty string, nan, etc...)
        - Creating a geometry column containing a point for each lat/lon
    '''
    df = df[df[lat_col].astype(bool)]
    df = df[df[lon_col].astype(bool)]
    df.geometry = gpd.points_from_xy(df[lon_col], df[lat_col])
    return df

def get_hover_string_list(df, hover_columns):
    result = []
    for index, row in df.iterrows():
        s = ""
        for col in hover_columns:
            if col in row:
                if col == "TA_Storage":
                    s += f"CO2 Storage (Mt) = {row[col]}<br>"
                else:   
                    s += f"{col} = {row[col]}<br>"
        result.append(s)
    return result