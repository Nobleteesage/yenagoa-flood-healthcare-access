import geopandas as gpd

pre = gpd.read_file("data/osm/access_pre_flood.gpkg")
post = gpd.read_file("data/osm/access_post_flood.gpkg")

# Fix self-intersecting/wrong-winding polygons before measuring area
pre["geometry"] = pre.geometry.buffer(0)
post["geometry"] = post.geometry.buffer(0)

pre_by_level = pre.dissolve(by="cost_level", aggfunc="first")
post_by_level = post.dissolve(by="cost_level", aggfunc="first")

pre_by_level["geometry"] = pre_by_level.geometry.buffer(0)
post_by_level["geometry"] = post_by_level.geometry.buffer(0)

print(f"{'Time (min)':<12}{'Pre-flood km2':<16}{'Post-flood km2':<16}{'Change km2':<14}{'Change %':<10}")
for level in sorted(pre_by_level.index):
    minutes = level / 60
    pre_area = abs(pre_by_level.loc[level, "geometry"].area) / 1_000_000
    if level in post_by_level.index:
        post_area = abs(post_by_level.loc[level, "geometry"].area) / 1_000_000
    else:
        post_area = 0.0
    change = post_area - pre_area
    pct = (change / pre_area * 100) if pre_area != 0 else 0
    print(f"{minutes:<12.0f}{pre_area:<16.2f}{post_area:<16.2f}{change:<14.2f}{pct:<10.1f}")
