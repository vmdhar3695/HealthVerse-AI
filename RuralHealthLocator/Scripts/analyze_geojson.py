
import json
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Data_Cleaned" / "india_healthcare_facilities.geojson"
OUTPUT_DIR = BASE_DIR / "Outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

features = data.get("features", [])

total = len(features)
missing_name = 0
missing_coordinates = 0
missing_type = 0
duplicate_ids = 0

state_counts = Counter()
type_counts = Counter()
seen_ids = set()

for feature in features:
    props = feature.get("properties") or {}
    geometry = feature.get("geometry") or {}

    # Facility name
    name = props.get("name")
    if not name or not str(name).strip():
        missing_name += 1

    # Coordinates
    coordinates = geometry.get("coordinates")
    if not coordinates:
        missing_coordinates += 1

    # Facility type
    facility_type = (
        props.get("amenity")
        or props.get("healthcare")
        or "Unknown"
    )
    type_counts[str(facility_type)] += 1

    if facility_type == "Unknown":
        missing_type += 1

    # State/UT
    state = props.get("source_state_ut", "Unknown")
    state_counts[state] += 1

    # Duplicate OSM element IDs
    osm_id = props.get("@id")
    if osm_id is None:
        osm_id = props.get("id")

    if osm_id is not None:
        if osm_id in seen_ids:
            duplicate_ids += 1
        else:
            seen_ids.add(osm_id)

print("\n===== DATA QUALITY REPORT =====")
print("Total facilities:", total)
print("Missing names:", missing_name)
print("Missing coordinates:", missing_coordinates)
print("Missing facility types:", missing_type)
print("Repeated OSM IDs:", duplicate_ids)

print("\n===== FACILITY TYPE DISTRIBUTION =====")
for key, value in type_counts.most_common():
    print(key, ":", value)

print("\n===== STATE-WISE DISTRIBUTION =====")
for key, value in sorted(state_counts.items()):
    print(key, ":", value)

report = {
    "total_facilities": total,
    "missing_names": missing_name,
    "missing_coordinates": missing_coordinates,
    "missing_facility_types": missing_type,
    "repeated_osm_ids": duplicate_ids,
    "facility_type_distribution": dict(type_counts),
    "state_wise_distribution": dict(state_counts)
}

report_file = OUTPUT_DIR / "data_quality_report.json"

with open(report_file, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4, ensure_ascii=False)

print("\nReport saved at:", report_file)
