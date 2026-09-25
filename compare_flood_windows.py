import geopandas as gpd
import glob
import os

boundary = gpd.read_file("data/yenagoa_boundary.geojson")

flood_dir = "data/flood/FL20221019NGA_SHP"
flood_files = sorted(glob.glob(f"{flood_dir}/*MaximumFloodWaterExtent*.shp"))
cloud_files = sorted(glob.glob(f"{flood_dir}/*CloudObstruction*.shp"))

print("=== Flood water extent by time window, clipped to Yenagoa ===")
for f in flood_files:
    gdf = gpd.read_file(f)
    gdf = gdf.to_crs(boundary.crs)
    clipped = gpd.clip(gdf, boundary)
    total_area_ha = clipped.geometry.area.sum() * 111320 * 111320 / 10000  # rough deg->m2->ha
    label = os.path.basename(f).replace("_Nigeria.shp", "")
    print(f"  {label}: {len(clipped)} features, ~{total_area_ha:.1f} ha")

print("\n=== Cloud obstruction by time window, clipped to Yenagoa ===")
for f in cloud_files:
    gdf = gpd.read_file(f)
    gdf = gdf.to_crs(boundary.crs)
    clipped = gpd.clip(gdf, boundary)
    total_area_ha = clipped.geometry.area.sum() * 111320 * 111320 / 10000
    label = os.path.basename(f).replace("_Nigeria.shp", "")
    print(f"  {label}: {len(clipped)} features, ~{total_area_ha:.1f} ha")
