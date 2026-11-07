
import json
from pathlib import Path
from collections import Counter

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "Data_Raw"
OUTPUT_DIR = BASE_DIR / "Data_Cleaned"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

all_features = []
state_counts = Counter()
errors = []

# Read every GeoJSON file
geojson_files = sorted(RAW_DIR.glob("*.geojson"))

print("Total GeoJSON files found:", len(geojson_files))

for file_path in geojson_files:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if data.get("type") != "FeatureCollection":
            print("Skipped (not FeatureCollection):", file_path.name)
            errors.append(file_path.name)
            continue

        state_name = file_path.stem.replace(
            "_healthcare", ""
        ).replace("_", " ").title()

        features = data.get("features", [])

        for feature in features:
            properties = feature.setdefault("properties", {})

            # Preserve original properties and add source details
            properties["source_state_ut"] = state_name
            properties["source_file"] = file_path.name

            all_features.append(feature)

        state_counts[state_name] = len(features)

        print(f"{state_name}: {len(features)} facilities")

    except Exception as error:
        print("Error reading:", file_path.name, error)
        errors.append(file_path.name)

# Create combined GeoJSON
combined_data = {
    "type": "FeatureCollection",
    "features": all_features
}

output_file = OUTPUT_DIR / "india_healthcare_facilities.geojson"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(combined_data, file, ensure_ascii=False)

print("\n----- MERGE SUMMARY -----")
print("Files processed:", len(state_counts))
print("Total facilities:", len(all_features))
print("Files with errors:", len(errors))
print("Output saved at:", output_file)

print("\nState-wise facility counts:")
for state, count in sorted(state_counts.items()):
    print(state, ":", count)
