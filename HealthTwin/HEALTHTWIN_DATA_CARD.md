# DATA CARD – HEALTHTWIN AI
## Synthetic Electronic Health Records (EHR) Dataset

### 1. Dataset Identification

| Attribute | Details |
|---|---|
| Project Name | HealthVerse AI |
| Module Name | HealthTwin AI |
| Dataset Name | Synthea Synthetic EHR Dataset |
| Dataset Version | v4.0.0 (as provided) |
| Package Name | `synthea_sample_data_csv_apr2020` |
| Data Format | CSV |
| Download Date | 07 November 2026 |
| Dataset Type | Synthetic Healthcare Data |
| Primary Source | Synthea |

**Official Source:** https://synthetichealth.github.io/synthea/#about-landing

### 2. Dataset Description

The Synthea Synthetic EHR Dataset contains artificially generated electronic health records representing fictional patients. It includes demographic details, medical encounters, clinical observations, health conditions, and medication information.

This dataset is used in the HealthTwin AI module to explore patient health records, analyze health parameters, identify health patterns, and support the development of AI-based preventive healthcare applications.

Since the records are synthetically generated, they do not represent actual individual patient medical records.

### 3. Dataset Structure

The downloaded dataset contains five primary CSV files.

| CSV File | Original Records | Columns |
|---|---:|---:|
| patients.csv | 1,171 | 25 |
| encounters.csv | 53,346 | 15 |
| observations.csv | 299,697 | 8 |
| conditions.csv | 8,376 | 6 |
| medications.csv | 42,989 | 13 |
| **Total** | **405,579** | — |

After removing exact duplicate rows from observations.csv, the cleaned dataset contains **405,137 records**.

### 4. Important Dataset Attributes

**Patients**
- Patient ID
- Birth date
- Gender
- City
- State
- ZIP code
- Marital status

**Encounters**
- Encounter ID
- Patient ID
- Encounter start and end dates
- Encounter class
- Encounter description
- Reason for encounter

**Observations**
- Patient ID
- Encounter ID
- Observation date
- Observation category
- Observation code
- Description
- Value
- Units

**Conditions**
- Patient ID
- Encounter ID
- Condition code
- Description
- Start date
- Stop date

**Medications**
- Patient ID
- Encounter ID
- Medication code
- Description
- Start date
- Stop date
- Reason for medication

### 5. Observed Population Profile

The dataset contains 1,171 synthetic patient records.

**Gender Distribution**

| Gender | Patient Count | Percentage |
|---|---:|---:|
| Female | 609 | 52.01% |
| Male | 562 | 47.99% |
| **Total** | **1,171** | **100%** |

**Geographical Distribution**
- State: Massachusetts, USA
- Patients from Massachusetts: 1,171
- Unique cities: 237

**Birth Date Range**
- Earliest birth date: 1909-12-22
- Latest birth date: 2020-03-22

The original population-generation settings, including seed and custom generation parameters, were not available in the downloaded package and could not be verified.

### 6. Data Quality Assessment

The dataset was examined for missing values, duplicate records, and date validity.

**6.1 Missing Values**

The following missing values were identified in the original datasets:

| Dataset | Column | Missing Values |
|---|---|---:|
| Patients | DEATHDATE | 1,000 |
| Patients | DRIVERS | 213 |
| Patients | PASSPORT | 273 |
| Patients | PREFIX | 244 |
| Patients | SUFFIX | 1,159 |
| Patients | MAIDEN | 840 |
| Patients | MARITAL | 380 |
| Patients | ZIP | 543 |
| Encounters | REASONCODE | 39,569 |
| Encounters | REASONDESCRIPTION | 39,569 |
| Observations | ENCOUNTER | 30,363 |
| Observations | UNITS | 12,735 |
| Conditions | STOP | 3,811 |
| Medications | STOP | 1,895 |
| Medications | REASONCODE | 11,117 |
| Medications | REASONDESCRIPTION | 11,117 |

Missing values were retained for further consideration rather than blindly replacing them. For example, a missing condition or medication stop date may indicate an ongoing record.

**6.2 Duplicate Analysis**

- Exact duplicate records were identified in observations.csv.
- A total of 442 exact duplicate rows were removed.
- Other datasets were examined as part of the duplicate analysis.
- Repeated health observations at different dates were not treated as duplicates.

**6.3 Date Validation**

Date columns were converted and checked for invalid date values in the inspected fields. No invalid dates were identified in those checks. Missing dates were retained.

### 7. Data Cleaning and Preprocessing Performed

The following operations were completed:

1. Loaded all five CSV datasets using Pandas.
2. Examined dataset dimensions and column information.
3. Analyzed missing values.
4. Identified exact duplicate records.
5. Removed 442 exact duplicate observation rows.
6. Converted inspected date columns into appropriate date formats.
7. Checked date validity.
8. Saved cleaned datasets in the Cleaned_Data folder.
9. Saved date-converted datasets in the Preprocessed_Data folder.

**Note:** Numerical scaling, categorical encoding, general missing-value imputation, and model-specific feature engineering have not yet been performed.

### 8. Exploratory Data Analysis (EDA)

Exploratory Data Analysis was performed to understand the structure and distribution of the healthcare data.

The following visualizations were generated:

- Patient age distribution
- Gender distribution
- Top 10 most common medical conditions
- Observation value distribution
- Blood pressure distribution
- Heart rate distribution
- Observation types distribution

These visualizations help understand patient demographics, common health conditions, and the distribution of clinical measurements.

### 9. Health Parameter Coverage

The availability of important health parameters was examined for the 1,171 patients.

| Health Parameter | Available Patients | Coverage |
|---|---:|---:|
| Systolic Blood Pressure | 1,171 | 100% |
| Diastolic Blood Pressure | 1,171 | 100% |
| Heart Rate | 1,171 | 100% |
| BMI | 1,134 | 96.84% |
| Body Height | 1,171 | 100% |
| Body Weight | 1,171 | 100% |

The dataset provides good coverage of several important health parameters, making it useful for exploratory analysis and future HealthTwin model development.

### 10. Source and Licence Information

- Dataset provider: Synthea
- Official website: https://synthetichealth.github.io/synthea/
- Downloaded package: `synthea_sample_data_csv_apr2020`
- Dataset format: CSV
- Download date: 07 November 2026

The official Synthea download documentation describes its generated datasets as available for unrestricted secondary use. No separate licence file was found inside the downloaded ZIP package.

The Synthea software licence should not be confused with the usage terms of the generated data.

### 11. Additional Dataset – MIMIC-IV

MIMIC-IV is an additional clinical dataset available through PhysioNet.

| Attribute | Status |
|---|---|
| Dataset | MIMIC-IV |
| Source | PhysioNet |
| Account creation | Not completed |
| Credentialing | Not completed |
| Dataset access | Not accessed |
| Used in current analysis | No |

MIMIC-IV is not included in the current HealthTwin analysis. It may be considered in future research after completing the required PhysioNet access and credentialing process.

### 12. Limitations

1. The dataset contains synthetic records and does not represent actual patient medical histories.
2. The geographical distribution is limited to Massachusetts, USA.
3. Some demographic and clinical attributes contain missing values.
4. The original population-generation configuration could not be verified.
5. Synthetic data may not fully represent the complexity and diversity of real-world clinical data.
6. MIMIC-IV has not been accessed or incorporated into the current analysis.
7. Additional preprocessing and validation will be required before training machine learning models.

### 13. Intended Use in HealthTwin AI

The dataset is intended to support research and development activities within the HealthTwin AI module.

Potential applications include:

- Patient health record analysis.
- Monitoring vital health parameters.
- Analyzing historical health observations.
- Identifying patterns in patient health data.
- Developing preventive healthcare prediction models.
- Supporting future digital health twin representations.

The dataset is intended for research and educational development, not for direct clinical diagnosis or treatment decisions.

### 14. Project Folder Organization

The HealthTwin module currently contains the following folders and files:

- `Data/` – Original downloaded CSV datasets.
- `Cleaned_Data/` – Cleaned CSV datasets.
- `Preprocessed_Data/` – Date-converted datasets.
- `Outputs/` – Generated analysis outputs and visualizations.
- `analysis.py` – Dataset analysis and EDA script.
- `check_population_details.py` – Population profile inspection script.

### 15. References

1. Synthea. Official Synthetic Patient Generation Project. https://synthetichealth.github.io/synthea/
2. Walonoski, J., et al. (2018). Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record. *Journal of the American Medical Informatics Association*, 25(3), 230–238. https://doi.org/10.1093/jamia/ocx079
3. Synthea GitHub Repository. https://github.com/synthetichealth/synthea

### 16. Completion Summary

The Synthea Synthetic EHR dataset has been downloaded, inspected, cleaned, and analyzed for the HealthTwin AI module. Missing-value analysis, duplicate removal, date validation, exploratory data analysis, health parameter coverage analysis, and population profiling have been completed.

The dataset source, observed characteristics, preprocessing activities, limitations, and MIMIC-IV access status have been documented.
