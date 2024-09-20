import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# Load data
gdf_gare = gpd.read_file('datasets/last_data/gdf_gare.geojson')
gdf_region = gpd.read_file('datasets/last_data/gdf_region.geojson')

gdf_gare = gdf_gare.set_crs(epsg=4326)
gdf_region = gdf_region.set_crs(epsg=4326)

fig = px.choropleth(gdf_region,
                    geojson=gdf_region.geometry,
                    locations=gdf_region.index,
                    color='Prix par km',
                    labels={'Prix par km': 'Tarif par km'})

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(geo=dict(showframe=False, showcoastlines=False))

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Choropleth Map of Tarif par km"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='choropleth-map', figure=fig), width=12)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)