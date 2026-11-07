import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Data_Cleaned" / "india_healthcare_facilities.geojson"
OUTPUT_FILE = (
    BASE_DIR / "Data_Cleaned" / "india_healthcare_facilities_cleaned.geojson"
)
REPORT_FILE = BASE_DIR / "Outputs" / "india_healthcare_facilities_cleaning_report.json"

CATEGORY_ORDER = (
    "hospital",
    "clinic",
    "pharmacy",
    "doctors",
    "diagnostic_center",
    "blood_bank",
    "health_center",
    "other_healthcare",
    "manual_review",
)

HEALTHCARE_CATEGORY_MAP = {
    "hospital": "hospital",
    "homeo_hospital": "hospital",
    "clinic": "clinic",
    "homeo_clinic": "clinic",
    "pharmacy": "pharmacy",
    "chemist": "pharmacy",
    "dispensary": "pharmacy",
    "dispensory": "pharmacy",
    "homeo_dispensary": "pharmacy",
    "doctor": "doctors",
    "doctors": "doctors",
    "general_physician": "doctors",
    "general_practitioner": "doctors",
    "laboratory": "diagnostic_center",
    "medical_laboratory": "diagnostic_center",
    "diagnostic_center": "diagnostic_center",
    "medical_imaging": "diagnostic_center",
    "scan_center": "diagnostic_center",
    "sample_collection": "diagnostic_center",
    "blood_bank": "blood_bank",
    "blood_donation": "blood_bank",
    "health_post": "health_center",
    "health_centre": "health_center",
    "health_center": "health_center",
    "healthcare_center": "health_center",
    "healthcare_centre": "health_center",
    "health_care_center": "health_center",
    "health_care_centre": "health_center",
    "community_health_centre": "health_center",
    "community_health_center": "health_center",
    "primary_health_centre": "health_center",
    "primary_health_center": "health_center",
    "govt_primary_health_care_centre": "health_center",
    "health_sub_centre": "health_center",
    "health_sub_center": "health_center",
    "sub_centre": "health_center",
    "sub_center": "health_center",
    "vaccination_centre": "health_center",
    "vaccination_center": "health_center",
    "birthing_centre": "health_center",
    "birthing_center": "health_center",
    "fhc": "health_center",
    "f_h_c_health_centre": "health_center",
    "phc": "health_center",
}

OTHER_HEALTHCARE_TYPES = {
    "alternative",
    "audiologist",
    "ayurveda",
    "ayurvedic",
    "ayurvedic_doctor",
    "ayurvedic_treatment",
    "ayurved",
    "vedacare_ayurveda",
    "nutrition_counselling",
    "psychiatry",
    "counselling",
    "community_health_worker",
    "dentist",
    "dialysis",
    "dermatologist",
    "disability",
    "health_care_facility",
    "hospice",
    "homeopathy",
    "homoeopathic",
    "midwife",
    "nurse",
    "nursing",
    "nursing_home",
    "occupational_therapist",
    "optician",
    "optometrist",
    "orthologist",
    "palliative_care",
    "physiotherapist",
    "podiatrist",
    "psychotherapist",
    "rehabilitation",
    "skin_care",
    "smart_therapy_autism_centre",
    "speech_therapist",
    "therapist",
}

# Only explicit, clearly non-human-healthcare categories are removed.
UNRELATED_TYPES = {
    "fast_food",
    "marketplace",
    "monastery",
    "post_office",
    "veterinary",
    "veterinary_pharmacy",
}

CLASSIFICATION_TAG_KEYS = ("healthcare", "amenity", "shop", "office")
OSM_ELEMENT_TYPES = {"node", "way", "relation"}
AMBIGUOUS_TYPES = {
    "building",
    "childcare",
    "college",
    "research_institute",
    "social_facility",
    "yes",
}


def _normalize_value(value: Any) -> str:
    normalized = str(value).strip().casefold()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    return re.sub(r"_+", "_", normalized).strip("_")


def _tag_values(properties: dict[str, Any], key: str) -> list[str]:
    value = properties.get(key)
    if value is None:
        return []
    return [
        normalized
        for part in str(value).split(";")
        if (normalized := _normalize_value(part))
    ]


def _osm_identity(feature: dict[str, Any]) -> tuple[str, str] | None:
    properties = feature.get("properties")
    if not isinstance(properties, dict):
        properties = {}

    explicit_type = (
        properties.get("@type")
        or properties.get("osm_type")
        or properties.get("element_type")
    )
    element_type = _normalize_value(explicit_type) if explicit_type else ""
    candidates = (
        properties.get("@id"),
        feature.get("id"),
        properties.get("id"),
        properties.get("osm_id"),
    )

    for candidate in candidates:
        if candidate is None:
            continue
        candidate_text = str(candidate).strip().casefold()
        match = re.fullmatch(r"(node|way|relation)/([1-9]\d*)", candidate_text)
        if match:
            return match.group(1), match.group(2)
        if (
            element_type in OSM_ELEMENT_TYPES
            and re.fullmatch(r"[1-9]\d*", candidate_text)
        ):
            return element_type, candidate_text
    return None


def _classify(properties: dict[str, Any]) -> tuple[str | None, str | None]:
    values_by_key = {
        key: _tag_values(properties, key) for key in CLASSIFICATION_TAG_KEYS
    }

    for key in CLASSIFICATION_TAG_KEYS:
        for value in values_by_key[key]:
            if key == "healthcare" and value in {"centre", "center"}:
                return "health_center", None
            category = HEALTHCARE_CATEGORY_MAP.get(value)
            if category:
                return category, None
            if value in OTHER_HEALTHCARE_TYPES:
                return "other_healthcare", None
        if key == "shop":
            if "medical_supply" in values_by_key[key]:
                return "other_healthcare", None
            if "optician" in values_by_key[key]:
                return "other_healthcare", None
        if key == "office" and any(
            value in {"therapist", "homeopath"} for value in values_by_key[key]
        ):
            return "other_healthcare", None

    all_values = [
        (key, value)
        for key in CLASSIFICATION_TAG_KEYS
        for value in values_by_key[key]
    ]
    ambiguous_values = [
        (key, value) for key, value in all_values if value in AMBIGUOUS_TYPES
    ]
    if ambiguous_values:
        details = ", ".join(f"{key}={value}" for key, value in ambiguous_values)
        return "manual_review", f"ambiguous healthcare tags: {details}"

    if any(value in {"healthcare", "health_care"} for _, value in all_values):
        return "other_healthcare", None

    uncertain_values = [
        (key, value)
        for key, value in all_values
        if value not in UNRELATED_TYPES
    ]
    if uncertain_values:
        details = ", ".join(f"{key}={value}" for key, value in uncertain_values)
        return "manual_review", f"unclassified or ambiguous healthcare tags: {details}"

    if all_values:
        details = ", ".join(f"{key}={value}" for key, value in all_values)
        return None, f"clearly unrelated tags: {details}"
    return "manual_review", "no recognized healthcare classification tags"


def _is_position(value: Any) -> tuple[bool, str | None]:
    if not isinstance(value, list) or len(value) < 2:
        return False, "coordinate position must contain longitude and latitude"
    if any(
        isinstance(component, bool)
        or not isinstance(component, (int, float))
        or (isinstance(component, float) and not math.isfinite(component))
        for component in value
    ):
        return False, "coordinate position contains a non-finite or non-numeric value"
    longitude, latitude = value[0], value[1]
    if not -180 <= longitude <= 180:
        return False, f"longitude {longitude} is outside [-180, 180]"
    if not -90 <= latitude <= 90:
        return False, f"latitude {latitude} is outside [-90, 90]"
    return True, None


def _validate_line(coordinates: Any, minimum_positions: int) -> str | None:
    if not isinstance(coordinates, list) or len(coordinates) < minimum_positions:
        return f"expected at least {minimum_positions} coordinate positions"
    for position in coordinates:
        valid, reason = _is_position(position)
        if not valid:
            return reason
    return None


def _validate_polygon(coordinates: Any) -> str | None:
    if not isinstance(coordinates, list) or not coordinates:
        return "polygon must contain at least one linear ring"
    for ring_index, ring in enumerate(coordinates):
        reason = _validate_line(ring, 4)
        if reason:
            return f"ring {ring_index}: {reason}"
        if ring[0] != ring[-1]:
            return f"ring {ring_index} is not closed"
    return None


def _validate_geometry(geometry: Any) -> tuple[bool, str | None]:
    if geometry is None:
        return False, "geometry is missing or null"
    if not isinstance(geometry, dict):
        return False, "geometry must be an object or null"

    geometry_type = geometry.get("type")
    coordinates = geometry.get("coordinates")
    if geometry_type == "Point":
        valid, reason = _is_position(coordinates)
        return valid, reason
    if geometry_type == "LineString":
        reason = _validate_line(coordinates, 2)
        return reason is None, reason
    if geometry_type == "Polygon":
        reason = _validate_polygon(coordinates)
        return reason is None, reason
    if geometry_type == "MultiPolygon":
        if not isinstance(coordinates, list) or not coordinates:
            return False, "MultiPolygon must contain at least one polygon"
        for polygon_index, polygon in enumerate(coordinates):
            reason = _validate_polygon(polygon)
            if reason:
                return False, f"polygon {polygon_index}: {reason}"
        return True, None
    return False, f"unsupported geometry type: {geometry_type!r}"


def _state_name(properties: dict[str, Any]) -> str:
    state = (
        properties.get("source_state_ut")
        or properties.get("addr:state")
        or properties.get("state")
    )
    return str(state).strip() if state is not None and str(state).strip() else "Unknown"


def _record_details(
    index: int, feature: dict[str, Any], properties: dict[str, Any]
) -> dict[str, Any]:
    identity = _osm_identity(feature)
    osm_type, osm_id = identity if identity is not None else (None, None)
    return {
        "feature_index": index,
        "osm_type": osm_type,
        "osm_id": osm_id,
        "name": properties.get("name"),
        "state": _state_name(properties),
    }


def _load_input() -> tuple[dict[str, Any], list[Any]]:
    try:
        with INPUT_FILE.open("r", encoding="utf-8") as input_file:
            data = json.load(input_file)
    except OSError as error:
        raise OSError(f"Unable to read input GeoJSON {INPUT_FILE}: {error}") from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Malformed JSON in {INPUT_FILE} at line {error.lineno}, "
            f"column {error.colno}: {error.msg}"
        ) from error

    if not isinstance(data, dict) or data.get("type") != "FeatureCollection":
        raise ValueError(
            f"Expected a GeoJSON FeatureCollection in {INPUT_FILE}"
        )
    features = data.get("features")
    if not isinstance(features, list):
        raise ValueError(f"Expected 'features' to be a list in {INPUT_FILE}")
    return data, features


def clean_geojson() -> dict[str, Any]:
    _, features = _load_input()

    seen_osm_ids: dict[tuple[str, str], int] = {}
    cleaned_features = []
    duplicate_records = []
    duplicate_identities: set[tuple[str, str]] = set()
    unrelated_records = []
    geometry_review_records = []
    manual_review_records = []
    category_distribution: Counter[str] = Counter()
    state_category_distribution: dict[str, Counter[str]] = defaultdict(Counter)
    missing_name_count = 0
    retained_missing_name_count = 0
    duplicates_removed = 0
    unrelated_records_removed = 0

    for index, feature in enumerate(features):
        if not isinstance(feature, dict) or feature.get("type") != "Feature":
            raise ValueError(f"Feature at index {index} is not a GeoJSON Feature")
        source_properties = feature.get("properties")
        if source_properties is not None and not isinstance(source_properties, dict):
            raise ValueError(
                f"Feature at index {index} has 'properties' that is not an object or null"
            )
        properties = source_properties if isinstance(source_properties, dict) else {}
        if "cleaned_category" in properties:
            raise ValueError(
                f"Feature at index {index} already has 'cleaned_category'; "
                "refusing to overwrite an original property"
            )

        name = properties.get("name")
        has_name = name is not None and bool(str(name).strip())
        if not has_name:
            missing_name_count += 1

        details = _record_details(index, feature, properties)
        geometry_valid, geometry_reason = _validate_geometry(feature.get("geometry"))
        if not geometry_valid:
            geometry_review_records.append(
                {**details, "reason": geometry_reason}
            )

        identity = _osm_identity(feature)
        if identity is not None and identity in seen_osm_ids:
            duplicates_removed += 1
            duplicate_identities.add(identity)
            duplicate_records.append(
                {
                    **details,
                    "duplicate_of_feature_index": seen_osm_ids[identity],
                }
            )
            continue
        if identity is not None:
            seen_osm_ids[identity] = index

        category, classification_reason = _classify(properties)
        if category is None:
            unrelated_records_removed += 1
            unrelated_records.append(
                {**details, "reason": classification_reason}
            )
            continue

        cleaned_feature = dict(feature)
        cleaned_properties = dict(properties)
        cleaned_properties["cleaned_category"] = category
        cleaned_feature["properties"] = cleaned_properties
        cleaned_features.append(cleaned_feature)
        category_distribution[category] += 1
        state_category_distribution[details["state"]][category] += 1
        if not has_name:
            retained_missing_name_count += 1

        review_reasons = []
        if category == "manual_review":
            review_reasons.append(classification_reason)
        if not geometry_valid:
            review_reasons.append(f"invalid or missing geometry: {geometry_reason}")
        if review_reasons:
            manual_review_records.append(
                {
                    **details,
                    "cleaned_category": category,
                    "reasons": review_reasons,
                }
            )

    output_count = len(cleaned_features)
    if len(features) != output_count + duplicates_removed + unrelated_records_removed:
        raise RuntimeError(
            "Cleaning count reconciliation failed: input count must equal output "
            "count plus duplicate and unrelated records removed"
        )
    if sum(category_distribution.values()) != output_count:
        raise RuntimeError("Category distribution does not match output count")

    output_data = {"type": "FeatureCollection", "features": cleaned_features}
    report = {
        "input_record_count": len(features),
        "output_record_count": output_count,
        "unrelated_records_removed": unrelated_records_removed,
        "unrelated_record_details": unrelated_records,
        "duplicate_records_identified": duplicates_removed,
        "duplicate_ids": [
            {"osm_type": osm_type, "osm_id": osm_id}
            for osm_type, osm_id in sorted(duplicate_identities)
        ],
        "duplicate_records": duplicate_records,
        "missing_name_count": missing_name_count,
        "retained_missing_name_count": retained_missing_name_count,
        "invalid_or_missing_geometry_count": len(geometry_review_records),
        "geometry_review_records": geometry_review_records,
        "manual_review_record_count": len(manual_review_records),
        "manual_review_records": manual_review_records,
        "category_distribution": {
            category: category_distribution.get(category, 0)
            for category in CATEGORY_ORDER
        },
        "state_wise_category_distribution": {
            state: {
                category: counts.get(category, 0)
                for category in CATEGORY_ORDER
            }
            for state, counts in sorted(state_category_distribution.items())
        },
        "count_reconciliation": {
            "input_record_count": len(features),
            "output_record_count": output_count,
            "duplicate_records_removed": duplicates_removed,
            "unrelated_records_removed": unrelated_records_removed,
            "reconciles": len(features)
            == output_count + duplicates_removed + unrelated_records_removed,
        },
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with OUTPUT_FILE.open("w", encoding="utf-8") as output_file:
            json.dump(output_data, output_file, ensure_ascii=False)
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with REPORT_FILE.open("w", encoding="utf-8") as report_file:
            json.dump(report, report_file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise OSError(f"Unable to write cleaning output or report: {error}") from error

    return report


if __name__ == "__main__":
    cleaning_report = clean_geojson()
    print(f"Cleaned GeoJSON saved to: {OUTPUT_FILE}")
    print(f"Cleaning report saved to: {REPORT_FILE}")
    print(
        "Cleaning summary: "
        f"{cleaning_report['input_record_count']} input, "
        f"{cleaning_report['output_record_count']} output, "
        f"{cleaning_report['unrelated_records_removed']} unrelated removed, "
        f"{cleaning_report['duplicate_records_identified']} duplicate records "
        f"identified, "
        f"{cleaning_report['invalid_or_missing_geometry_count']} invalid/missing "
        f"geometries, "
        f"{cleaning_report['manual_review_record_count']} records for manual review, "
        f"{cleaning_report['missing_name_count']} missing names"
    )
