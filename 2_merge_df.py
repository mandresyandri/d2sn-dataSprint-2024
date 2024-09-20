import pandas as pd
import geopandas as gpd
from shapely import wkt
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# Load data
df_1 = pd.read_csv("datasets/last_data/region_gare.csv")
df_2 = pd.read_csv("datasets/last_data/prix_par_km.csv")

merged_df = pd.merge(df_1, df_2, left_on="Code UIC", right_on="Gare destination - code UIC", how='left')

merged_df = merged_df.rename(columns={
    'nom': 'nom_region',
    'geometry_y': 'geo_shape',
    'geometry_x': 'geopoint'
})

merged_df = merged_df[[
    'Code UIC', 'geopoint', 'nom_region', 'geo_shape',
    'Destination', 'Prix par km']]

#####
# Calcul des prix avec un merge colonnes
#####
grouped_df = merged_df.groupby('nom_region')['Prix par km'].mean().reset_index()
grouped_df = grouped_df.rename(columns={'Prix par km': 'Prix moyen par km'})
merged_df = pd.merge(merged_df, grouped_df, on='nom_region', how='left')


merged_df['geopoint'] = merged_df['geopoint'].apply(wkt.loads)
merged_df['geo_shape'] = merged_df['geo_shape'].apply(wkt.loads)

gdf_gare = gpd.GeoDataFrame(merged_df, geometry='geopoint')
gdf_region = gpd.GeoDataFrame(merged_df, geometry='geo_shape')

# Export GeoDataFrames to files
gdf_gare.to_file("datasets/last_data/gdf_gare.geojson", driver="GeoJSON")
gdf_region.to_file("datasets/last_data/gdf_region.geojson", driver="GeoJSON")
