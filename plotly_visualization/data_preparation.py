from __future__ import annotations
from typing import Literal

import os

import geopandas as gpd
import pandas as pd 
import numpy as np
import json

import shapely
from shapely.geometry.base import GeometrySequence
from shapely.geometry.polygon import Polygon
from shapely.geometry.linestring import LineString


MOSCOW_REGIONS_GEOJSON = os.path.abspath('data/moscow_regions.geojson')
MOSCOW_PARKINGS_GEOJSON = os.path.abspath('data/moscow_parkings.geojson')

""" Functions """
def get_linestrings(feature) -> GeometrySequence | list[Polygon] | list[LineString] | Literal[False]:
    """ Function returns geometry data from geometry object in GeoDataFrame

    Returns:
        GeometrySequence: in case it's a multi-sth
        List[Polygon] or List[LineString]: in case it's a single figure of this kind
        Literal[False]: in case it's any other shape besides MultiPolygon, MultiLineString, Polygon or LineString
    """
    # Check if it's MultiPolygon or MultiLineString
    if isinstance(feature, shapely.geometry.multipolygon.MultiPolygon) or isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
        return feature.geoms
    # Check if it's Polygon or LineString
    elif isinstance(feature, feature, shapely.geometry.polygon.Polygon) or isinstance(feature, shapely.geometry.linestring.LineString):
        return [feature]
    # Other cases 
    else:
        return False


def get_parkingGraphData(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """ Func is made specially for Moscow street parkings GeoDataFrame to generate another GeoDataFrame which contains data for a graph"""
    
    # Lists to gather graph objects' latitude, longitude, name 
    lats, lons, names, zNumbers, carCaps, carDisCaps, addresses = list(), list(), list(), list(), list(), list(), list()

    # Iterate through the Moscow street parkings GeoDataFrame
    for feature, name, zNum, cCap, cDCap, address in zip(gdf.geometry, gdf.ParkingName, gdf.ParkingZoneNumber, gdf.CarCapacity, gdf.CarCapacityDisabled, gdf.Address):
        # Geometry objects of the parking  
        linestrings = get_linestrings(feature)
        if linestrings != False:
            # Iterate though every object in the geometry objects 
            for linestring in linestrings:
                x, y = linestring.xy
                # Append coordinates 
                lats = np.append(lats, y)
                lons = np.append(lons, x)
                names = np.append(names, [name]*len(y))
                zNumbers = np.append(zNumbers, [zNum]*len(y))
                carCaps = np.append(carCaps, [cCap]*len(y))
                carDisCaps = np.append(carDisCaps, [cDCap]*len(y))
                addresses = np.append(addresses, [address]*len(y))
                
                
                # Add line break to prevent connections between different parkings 
                lats = np.append(lats, None)
                lons = np.append(lons, None)
                names = np.append(names, None)
                zNumbers = np.append(zNumbers, None)
                carCaps = np.append(carCaps, None)
                carDisCaps = np.append(carDisCaps, None)
                addresses = np.append(addresses, None)

    # Create a new GeoDataFrame to save the graph data  
    graph_df = pd.DataFrame()
    graph_df['name'] = names
    graph_df['lon'] = lons
    graph_df['lat'] = lats
    graph_df['zNum'] = zNumbers
    graph_df['carCap'] = carCaps
    graph_df['carDisCap'] = carDisCaps
    graph_df['address'] = addresses
    
    return graph_df


def get_regionsGraphData(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """ Func is made specially for Moscow regions GeoDataFrame to generate another GeoDataFrame which contains data for a graph"""
    
    # Lists to gather graph objects' latitude, longitude, name 
    lats, lons, names = list(), list(), list()

    # Iterate through the Moscow street parkings GeoDataFrame
    for feature, name in zip(gdf.geometry, gdf.name):
        # Geometry objects of the parking  
        linestrings = get_linestrings(feature)
        if linestrings != False:
            # Iterate though every object in the geometry objects
            for linestring in linestrings:
                x, y = linestring.boundary.xy
                # Append coordinates 
                lats = np.append(lats, y)
                lons = np.append(lons, x)
                names = np.append(names, [name]*len(y))
                # Add line break to prevent connections between different parkings 
                lats = np.append(lats, None)
                lons = np.append(lons, None)
                names = np.append(names, None)

     # Create a new GeoDataFrame to save the graph data  
    graph_df = pd.DataFrame()
    graph_df['name'] = names
    graph_df['lon'] = lons
    graph_df['lat'] = lats
    
    return graph_df


""" Code """
# if __name__ == '__main__':
# Opening and preprocessing Moscow regions GDF
regs_gdf = gpd.read_file(MOSCOW_REGIONS_GEOJSON)
regs_gdf.drop(columns = ['name_lat', 'created_at', 'updated_at', 'cartodb_id'], inplace=True)

# Opening and preprocessing Moscow street parkings GDF
parks_gdf = gpd.read_file(MOSCOW_PARKINGS_GEOJSON)[['Attributes', 'geometry']]

for attr in ['ParkingName', 'ParkingZoneNumber', 'CarCapacity', 'CarCapacityDisabled', 'Address']:
    parks_gdf[attr] = parks_gdf['Attributes'].apply(lambda x: x.get(attr))
parks_gdf.drop(columns=['Attributes'], inplace=True)

parks_gdf.Address = parks_gdf.Address.str.replace('город Москва, ', '')

# Count quantiles 
q_25 = parks_gdf['CarCapacity'].quantile(0.25)
q_50 = parks_gdf['CarCapacity'].quantile(0.50)
q_75 = parks_gdf['CarCapacity'].quantile(0.75)

# Split parkings GDF into 4 parts depending on CarCapacity 
parks_graphData_tiny = get_parkingGraphData(gdf=parks_gdf[parks_gdf['CarCapacity'] <= q_25])
parks_graphData_small = get_parkingGraphData(gdf=parks_gdf[(parks_gdf['CarCapacity'] > q_25) & (parks_gdf['CarCapacity'] <= q_50)])
parks_graphData_meduim = get_parkingGraphData(gdf=parks_gdf[(parks_gdf['CarCapacity'] > q_50) & (parks_gdf['CarCapacity'] <= q_75)])
parks_graphData_big = get_parkingGraphData(gdf=parks_gdf[parks_gdf['CarCapacity'] > q_75])

# Gather regs data 
regs_graphData = get_regionsGraphData(gdf=regs_gdf)
    
# Save dfs to csv
parks_graphData_tiny.to_csv('plotly_visualization/data/parkings_tiny.csv')
parks_graphData_small.to_csv('plotly_visualization/data/parkings_small.csv')
parks_graphData_meduim.to_csv('plotly_visualization/data/parkings_medium.csv')
parks_graphData_big.to_csv('plotly_visualization/data/parkings_big.csv')
regs_graphData.to_csv('plotly_visualization/data/regs.csv')

quantiles = {
    'q1': q_25,
    'q2': q_50,
    'q3': q_75,
}

with open('plotly_visualization/data/quantiles.json', 'w') as q_file:
    json.dump(quantiles, q_file)