import geopandas as gpd

roads_pre = gpd.read_file("data/osm/roads_pre_flood_timed.shp")
roads_post = gpd.read_file("data/osm/roads_post_flood_timed.shp")
hospitals = gpd.read_file("data/osm/hospitals.shp")

utm_crs = roads_pre.estimate_utm_crs()
print(f"Using projected CRS: {utm_crs}")

roads_pre = roads_pre.to_crs(utm_crs)
roads_post = roads_post.to_crs(utm_crs)
hospitals = hospitals.to_crs(utm_crs)

hospitals["hosp_id"] = range(1, len(hospitals) + 1)

roads_pre.to_file("data/osm/roads_pre_qneat.shp")
roads_post.to_file("data/osm/roads_post_qneat.shp")
hospitals.to_file("data/osm/hospitals_qneat.shp")

print(f"Roads (pre-flood): {len(roads_pre)} segments")
print(f"Roads (post-flood): {len(roads_post)} segments")
print(f"Hospitals: {len(hospitals)} points, IDs 1 to {len(hospitals)}")
