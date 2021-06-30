
import geopandas as gpd
import pandas as pd
from utils import *
from render import *
import os

from shapely.geometry import Point, Polygon




def plants_per_basin():
    '''
        pull basin and power pland dataframes
        For each basin, find all relevant power plants
        use polygon from shapley to see if geolocation is within basin
    '''
    dfs = load_dfs(os.path.join("Data", "config.json"))

    df_basin = dfs["USGS Sedimentary Basins 2012"]
    basin_names = df_basin.Name.unique()
    df_emission = dfs["EPA Power Plant Annual Emissions 2020"]

    exp_basin = df_basin.explode()

    co2_list = []
    storage_list = []
    names = []
    #return dataframe
    columns = ["name", "emissions", "storage"]
    df = pd.DataFrame(columns=columns)

    for index, basin_row in exp_basin.iterrows():
        co2_short_tons = 0.0
        #create polygon of basin area
        coords = basin_row['geometry']
        poly = Polygon(coords)

        for index, plant_row in df_emission.iterrows():
            lat= plant_row["Facility Latitude"]
            lon = plant_row["Facility Longitude"]
            the_point = Point(float(lon), float(lat))
            #check if plant within basin polygon
            if poly.contains(the_point) and float(plant_row["CO2 (Mt)" ]) > 0.0:
                co2_short_tons += float(plant_row["CO2 (Mt)" ])

        if co2_short_tons > 0.0 and basin_row["TA_Storage"] > 0.0:
            names.append(str(basin_row["Name"]))
            storage_list.append(float(basin_row["TA_Storage"]))
            co2_list.append(co2_short_tons)
        
    df["name"] = names
    df["emissions"] = co2_list
    df["storage"] = storage_list

    return df

# Uncomment to run code and write to csv file
'''
plants_per_basin_frame = plants_per_basin().to_csv("plants_per_basin.csv")   
'''