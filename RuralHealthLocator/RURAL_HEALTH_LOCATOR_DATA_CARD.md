# Rural Health Locator – Dataset Data Card

## 1. Dataset Overview

- **Project:** HealthVerse AI
- **Module:** Rural Health Locator
- **Dataset Name:** India Healthcare Facilities Dataset
- **Geographical Coverage:** 28 States and 8 Union Territories of India
- **Data Format:** GeoJSON
- **Primary Source:** OpenStreetMap (OSM)
- **Collection Method:** Overpass API queries using Overpass Turbo
- **Dataset Version:** 1.0
- **Collection Date:** 2026-11-07

## 2. Dataset Purpose

This dataset supports the Rural Health Locator module by providing geographical information about healthcare facilities across India.

It helps users identify nearby hospitals, clinics, pharmacies, doctors, diagnostic centres and other healthcare facilities.

## 3. Dataset Statistics

| Metric | Value |
|---|---:|
| Original facilities collected | 140,465 |
| Cleaned facilities | 140,464 |
| Duplicate records identified | 1 |
| Records removed as unrelated | 0 |
| Missing names | 3,592 |
| Manual review records | 1,217 |
| Invalid or missing geometries | 0 |

## 4. Facility Categories

The cleaned dataset contains:

- Hospitals
- Clinics
- Pharmacies
- Doctors
- Diagnostic Centres
- Blood Banks
- Health Centres
- Other Healthcare Facilities
- Manual Review Records

## 5. Data Collection

Healthcare facility information was collected from OpenStreetMap using Overpass Turbo.

Queries were performed for all 28 Indian States and 8 Union Territories.

The collected GeoJSON files were merged into a single India-wide dataset.

## 6. Data Cleaning and Processing

The following operations were performed:

- Merged regional GeoJSON files.
- Checked missing facility names.
- Identified duplicate OSM records.
- Validated geographical geometries.
- Standardized healthcare facility categories.
- Retained ambiguous records for manual review.
- Generated data quality and cleaning reports.

The original merged dataset was preserved separately. Cleaning operations were performed on a separate output file.

## 7. Data Quality

- Missing coordinates: 0
- Invalid or missing geometries: 0
- Duplicate records identified: 1
- Missing facility names: 3,592
- Records requiring manual review: 1,217

Missing facility names do not necessarily indicate invalid facilities.

## 8. Known Limitations

- OpenStreetMap data may be incomplete or outdated.
- Some facilities may have missing names.
- Some healthcare tags require manual classification.
- Facility availability and operating hours are not guaranteed to be current.
- The dataset should not be treated as a complete official registry of Indian healthcare facilities.

## 9. Intended Uses

- Finding nearby healthcare facilities.
- Mapping healthcare infrastructure.
- Rural healthcare accessibility analysis.
- Supporting location-based healthcare services.
- Identifying geographical gaps in healthcare coverage.

## 10. Licensing and Attribution

### Data Source
OpenStreetMap (OSM)

### Data Licence
Open Database License (ODbL) 1.0.

### Attribution
© OpenStreetMap contributors

Source: https://www.openstreetmap.org/

Copyright and Licence: https://www.openstreetmap.org/copyright

### Licence Requirements
- OpenStreetMap contributors must be credited when the data is publicly used or distributed.
- The ODbL licence must be clearly identified.
- Redistribution of OSM data and derivative databases must comply with ODbL share-alike requirements.
- The project must distinguish OSM-derived data from independently sourced data.

### Usage Note
This dataset was collected from OpenStreetMap using Overpass Turbo. Its use and redistribution must comply with the ODbL 1.0 licence.

## 11. Related Files

- `Data_Raw/` – Original regional GeoJSON files.
- `Data_Cleaned/india_healthcare_facilities.geojson` – Merged dataset.
- `Data_Cleaned/india_healthcare_facilities_cleaned.geojson` – Cleaned dataset.
- `Outputs/data_quality_report.json` – Data quality report.
- `Outputs/india_healthcare_facilities_cleaning_report.json` – Cleaning report.
- `Scripts/merge_geojson.py` – Dataset merging script.
- `Scripts/analyze_geojson.py` – Data analysis script.
- `Scripts/clean_geojson.py` – Data cleaning script.

## 12. Conclusion

The India Healthcare Facilities Dataset provides a consolidated geographical dataset for the Rural Health Locator module of HealthVerse AI.

It covers all 36 Indian States and Union Territories and contains 140,464 cleaned facility records.

The dataset can support healthcare facility discovery, mapping and accessibility analysis.

## 13. Government Health Schemes Dataset

### Dataset Overview
- **Dataset Name:** India Government Health Schemes
- **File Name:** `india_government_health_schemes.csv`
- **Format:** CSV
- **Number of Records:** 13
- **Number of Columns:** 14
- **Geographical Coverage:** Central Government schemes and selected Andhra Pradesh State schemes.

### Dataset Information
The dataset contains information about government healthcare schemes and programmes in India.

It includes:
- Scheme name and identification number.
- Scheme level and category.
- Description and eligibility.
- Benefits and application process.
- Official website and source name.
- Last verification date.
- Geographical coverage and implementation status.

### Data Source
Information is compiled from government scheme portals and official government sources. Individual scheme details and implementation status require verification against their respective official sources.

### Limitations
- Scheme eligibility and benefits may change over time.
- Implementation may vary between States and Union Territories.
- Some scheme details require further official verification.
- The dataset should not be treated as a substitute for official scheme guidelines.

### Related File
`Data_Raw/government_schemes/india_government_health_schemes.csv`


