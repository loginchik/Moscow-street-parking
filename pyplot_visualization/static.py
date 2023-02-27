import matplotlib.pyplot as plt
import geopandas as gpd 

# Create geopandas dataframes
regions_gdf = gpd.read_file(filename='data/moscow_regions.geojson')
regions_gdf.drop(columns = ['name_lat', 'created_at', 'updated_at', 'cartodb_id'], inplace=True)

parkings_gdf = gpd.read_file(filename='data/moscow_parkings.geojson')['geometry']

# Create graph
figure, axes = plt.subplots(1, figsize=(20, 20))

regsmap_sets = {
    'facecolor': 'white', 
    'edgecolor': 'black',
}

parks_sets = {
    'color': '#36162E',
    'linewidth': 1, 
}

regs_map = regions_gdf.plot(ax=axes, **regsmap_sets)
parkings_gdf.plot(ax=regs_map, markersize=5, label = 'Парковка', **parks_sets)

axes.set_title('Карта платных парковок г. Москва')
axes.legend()


if __name__ == '__main__':
    figure.savefig('results/static_graph.png', dpi=300)
