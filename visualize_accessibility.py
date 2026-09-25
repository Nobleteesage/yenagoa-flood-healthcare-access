import rasterio
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

roads = gpd.read_file("data/osm/roads_with_flood_status.shp")
hospitals = gpd.read_file("data/osm/hospitals_qneat.shp")

with rasterio.open("data/osm/access_pre_flood_raster.tif") as src:
    pre = src.read(1)
    pre_transform = src.transform
    pre_crs = src.crs
    pre_nodata = src.nodata
    pre_extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

with rasterio.open("data/osm/access_post_flood_raster.tif") as src:
    post = src.read(1)
    post_extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

pre_masked = np.ma.masked_where(pre == pre_nodata, pre) / 60
post_masked = np.ma.masked_where(post == pre_nodata, post) / 60

roads_proj = roads.to_crs(pre_crs)
hospitals_proj = hospitals.to_crs(pre_crs)

norm = Normalize(vmin=0, vmax=60)
cmap = plt.cm.RdYlGn_r

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

for ax, data, extent, title in [
    (axes[0], pre_masked, pre_extent, "Before Flood"),
    (axes[1], post_masked, post_extent, "After Flood"),
]:
    im = ax.imshow(data, extent=extent, origin="upper", cmap=cmap, norm=norm)
    roads_proj[~roads_proj["flooded"]].plot(ax=ax, color="black", linewidth=0.2, alpha=0.4)
    hospitals_proj.plot(ax=ax, color="blue", markersize=40, marker="+", linewidth=1.5, zorder=5)
    ax.set_title(f"Travel Time to Nearest Hospital: {title}", fontsize=13)
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.axis("off")

cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=axes, orientation="horizontal",
                     fraction=0.05, pad=0.05, label="Travel time (minutes)")

plt.savefig("data/osm/accessibility_comparison.png", dpi=150, bbox_inches="tight")
print("Saved: data/osm/accessibility_comparison.png")
