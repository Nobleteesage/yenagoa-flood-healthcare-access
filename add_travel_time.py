import geopandas as gpd

SPEED_KMH = {
    "trunk": 60, "trunk_link": 50,
    "primary": 50, "primary_link": 40,
    "secondary": 45, "secondary_link": 35,
    "tertiary": 35, "tertiary_link": 30,
    "residential": 25,
    "unclassified": 25,
    "service": 15,
    "track": 10,
    "path": 5,
    "footway": 5,
    "living_street": 15,
}
DEFAULT_SPEED_KMH = 20

def add_time_field(in_path, out_path):
    gdf = gpd.read_file(in_path)

    gdf_m = gdf.to_crs(gdf.estimate_utm_crs())
    gdf["length_m"] = gdf_m.geometry.length

    gdf["speed_kmh"] = gdf["highway"].map(SPEED_KMH).fillna(DEFAULT_SPEED_KMH)
    gdf["time_sec"] = gdf["length_m"] / (gdf["speed_kmh"] * 1000 / 3600)

    gdf.to_file(out_path)
    print(f"{out_path}: {len(gdf)} segments, total length {gdf['length_m'].sum()/1000:.1f} km")

add_time_field("data/osm/roads.shp", "data/osm/roads_pre_flood_timed.shp")
add_time_field("data/osm/roads_post_flood.shp", "data/osm/roads_post_flood_timed.shp")
