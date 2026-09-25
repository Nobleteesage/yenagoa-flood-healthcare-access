import geopandas as gpd

roads = gpd.read_file("data/osm/roads.shp")
flood = gpd.read_file("data/flood/yenagoa_clipped/yenagoa_flood_final.shp")

roads = roads.to_crs(flood.crs)

flood_union = flood.geometry.union_all()

roads["flooded"] = roads.geometry.intersects(flood_union)

n_flooded = roads["flooded"].sum()
n_total = len(roads)
print(f"Total road segments: {n_total}")
print(f"Segments intersecting flood: {n_flooded} ({100 * n_flooded / n_total:.1f}%)")

roads.to_file("data/osm/roads_with_flood_status.shp")

roads_post_flood = roads[~roads["flooded"]]
roads_post_flood.to_file("data/osm/roads_post_flood.shp")

print(f"\nSaved full network with flood status: data/osm/roads_with_flood_status.shp")
print(f"Saved post-flood network (flooded roads removed): data/osm/roads_post_flood.shp")
print(f"Post-flood network has {len(roads_post_flood)} segments remaining")
