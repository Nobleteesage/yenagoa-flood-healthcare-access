import rasterio
import numpy as np

PIXEL_AREA_KM2 = (50 * 50) / 1_000_000  # 50m cell size from QNEAT3 run
THRESHOLDS_SEC = [600, 1200, 1800, 2400, 3000, 3600]

def load(path):
    with rasterio.open(path) as src:
        data = src.read(1)
        nodata = src.nodata
        valid = data != nodata if nodata is not None else np.isfinite(data)
        return data, valid

pre, pre_valid = load("data/osm/access_pre_flood_raster.tif")
post, post_valid = load("data/osm/access_post_flood_raster.tif")

print(f"{'Time (min)':<12}{'Pre-flood km2':<16}{'Post-flood km2':<16}{'Change km2':<14}{'Change %':<10}")
for t in THRESHOLDS_SEC:
    pre_area = np.sum((pre <= t) & pre_valid) * PIXEL_AREA_KM2
    post_area = np.sum((post <= t) & post_valid) * PIXEL_AREA_KM2
    change = post_area - pre_area
    pct = (change / pre_area * 100) if pre_area > 0 else 0
    print(f"{t/60:<12.0f}{pre_area:<16.2f}{post_area:<16.2f}{change:<14.2f}{pct:<10.1f}")
