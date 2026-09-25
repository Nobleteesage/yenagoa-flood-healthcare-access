import ee
import json

ee.Initialize(project="ee-goriola-obafemi-ogoniland")

gaul2 = ee.FeatureCollection("FAO/GAUL/2025/level2")
aoi = gaul2.filter(
    ee.Filter.And(
        ee.Filter.eq("GAUL1_NAME", "Bayelsa"),
        ee.Filter.eq("GAUL2_NAME", "Yenegoa"),
    )
)

count = aoi.size().getInfo()
print(f"Matched features: {count}")

geojson = aoi.getInfo()
with open("data/yenagoa_boundary.geojson", "w") as f:
    json.dump(geojson, f)

print("Saved: data/yenagoa_boundary.geojson")
