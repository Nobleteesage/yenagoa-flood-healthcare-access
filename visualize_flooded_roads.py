import geopandas as gpd
import matplotlib.pyplot as plt

roads = gpd.read_file("data/osm/roads_with_flood_status.shp")
hospitals = gpd.read_file("data/osm/hospitals_qneat.shp")
flood = gpd.read_file("data/flood/yenagoa_clipped/yenagoa_flood_final.shp")
boundary = gpd.read_file("data/yenagoa_boundary.geojson")

hospitals = hospitals.to_crs(boundary.crs)
roads = roads.to_crs(boundary.crs)
flood = flood.to_crs(boundary.crs)

fig, ax = plt.subplots(figsize=(10, 10))

boundary.boundary.plot(ax=ax, color="black", linewidth=1)
flood.plot(ax=ax, color="#2166ac", alpha=0.5, label="Flood extent (Oct 2022)")
roads[~roads["flooded"]].plot(ax=ax, color="grey", linewidth=0.4, label="Roads (unaffected)")
roads[roads["flooded"]].plot(ax=ax, color="#b2182b", linewidth=1.2, label="Roads (flooded)")
hospitals.plot(ax=ax, color="black", marker="+", markersize=60, linewidth=1.5, label="Hospitals/clinics")

ax.set_title("Yenagoa, Bayelsa State: Flood Extent and Affected Roads (October 2022)", fontsize=12)
ax.legend(loc="lower left", fontsize=9)
ax.axis("off")

plt.savefig("data/osm/study_area_context.png", dpi=100, bbox_inches="tight")
print("Saved: data/osm/study_area_context.png")
