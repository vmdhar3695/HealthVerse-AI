
import pandas as pd
import os
import matplotlib.pyplot as plt

# ---------------------------------
# 1. FOLDER SETUP
# ---------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "Data")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "Outputs")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

files = [
    "patients.csv",
    "encounters.csv",
    "observations.csv",
    "conditions.csv",
    "medications.csv"
]

datasets = {}
quality_reports = []

# ---------------------------------
# 2. DATASET OVERVIEW
# ---------------------------------

print("\n========== DATASET OVERVIEW ==========")

for file in files:

    path = os.path.join(DATA_FOLDER, file)

    if not os.path.exists(path):
        print(f"\n{file} NOT FOUND")
        continue

    try:
        df = pd.read_csv(path)
        datasets[file] = df

        print("\n===================================")
        print("FILE:", file)
        print("===================================")

        print("Total Records:", len(df))
        print("Total Columns:", len(df.columns))

        print("\nColumn Names:")
        print(df.columns.tolist())

        print("\nFirst 5 Records:")
        print(df.head())

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:", df.duplicated().sum())

        # ---------------------------------
        # 3. DATA QUALITY REPORT
        # ---------------------------------

        missing_count = df.isnull().sum()
        missing_percent = (missing_count / len(df) * 100) if len(df) else missing_count

        for column in df.columns:
            quality_reports.append({
                "File": file,
                "Column": column,
                "Missing_Count": missing_count[column],
                "Missing_Percentage": round(missing_percent[column], 2),
                "Unique_Values": df[column].nunique(),
                "Data_Type": str(df[column].dtype),
                "Duplicate_Rows": df.duplicated().sum()
            })

    except Exception as e:
        print(f"Error reading {file}: {e}")


# ---------------------------------
# 4. SAVE DATA QUALITY REPORT
# ---------------------------------

if quality_reports:

    quality_df = pd.DataFrame(quality_reports)

    report_path = os.path.join(
        OUTPUT_FOLDER, "data_quality_report.csv"
    )

    quality_df.to_csv(report_path, index=False)

    print("\nData quality report saved:", report_path)


# ---------------------------------
# 5. EDA - PATIENT AGE DISTRIBUTION
# ---------------------------------

if "patients.csv" in datasets:

    patients = datasets["patients.csv"].copy()

    if "BIRTHDATE" in patients.columns:

        patients["BIRTHDATE"] = pd.to_datetime(
            patients["BIRTHDATE"], errors="coerce"
        )

        # Reference date used only for this exploratory analysis.
        reference_date = pd.Timestamp.today().normalize()

        patients["AGE"] = (
            (reference_date - patients["BIRTHDATE"]).dt.days / 365.25
        )

        patients.loc[
            (patients["AGE"] < 0) | (patients["AGE"] > 120),
            "AGE"
        ] = pd.NA

        age_data = patients["AGE"].dropna()

        if not age_data.empty:

            plt.figure(figsize=(8, 5))
            plt.hist(age_data, bins=20, edgecolor="black")
            plt.title("Patient Age Distribution")
            plt.xlabel("Age")
            plt.ylabel("Number of Patients")
            plt.tight_layout()

            plt.savefig(
                os.path.join(OUTPUT_FOLDER, "age_distribution.png")
            )
            plt.close()

            print("\nAge distribution graph saved.")


# ---------------------------------
# 6. EDA - GENDER DISTRIBUTION
# ---------------------------------

if "patients.csv" in datasets:

    patients = datasets["patients.csv"]

    if "GENDER" in patients.columns:

        gender_counts = patients["GENDER"].dropna().value_counts()

        if not gender_counts.empty:

            plt.figure(figsize=(7, 5))
            gender_counts.plot(kind="bar", edgecolor="black")
            plt.title("Patient Gender Distribution")
            plt.xlabel("Gender")
            plt.ylabel("Number of Patients")
            plt.xticks(rotation=0)
            plt.tight_layout()

            plt.savefig(
                os.path.join(OUTPUT_FOLDER, "gender_distribution.png")
            )
            plt.close()

            print("Gender distribution graph saved.")


# ---------------------------------
# 7. EDA - TOP 10 CONDITIONS
# ---------------------------------

if "conditions.csv" in datasets:

    conditions = datasets["conditions.csv"]

    if "DESCRIPTION" in conditions.columns:

        condition_counts = (
            conditions["DESCRIPTION"]
            .dropna()
            .value_counts()
            .head(10)
        )

        if not condition_counts.empty:

            plt.figure(figsize=(10, 6))
            condition_counts.sort_values().plot(
                kind="barh", edgecolor="black"
            )

            plt.title("Top 10 Common Conditions")
            plt.xlabel("Number of Records")
            plt.ylabel("Condition")
            plt.tight_layout()

            plt.savefig(
                os.path.join(OUTPUT_FOLDER, "top_conditions.png")
            )
            plt.close()

            print("Top conditions graph saved.")


# ---------------------------------
# 8. EDA - OBSERVATION VALUES
# ---------------------------------

if "observations.csv" in datasets:

    observations = datasets["observations.csv"].copy()

    if "VALUE" in observations.columns:

        observations["VALUE_NUMERIC"] = pd.to_numeric(
            observations["VALUE"], errors="coerce"
        )

        values = observations["VALUE_NUMERIC"].dropna()

        if not values.empty:

            plt.figure(figsize=(8, 5))
            plt.hist(values, bins=30, edgecolor="black")

            plt.title("Observation Values Distribution")
            plt.xlabel("Observation Value")
            plt.ylabel("Frequency")
            plt.tight_layout()

            plt.savefig(
                os.path.join(OUTPUT_FOLDER, "observation_distribution.png")
            )
            plt.close()

            print("Observation distribution graph saved.")


# ---------------------------------
# 9. FINAL STATUS
# ---------------------------------

print("\n========== ANALYSIS COMPLETED ==========")
print("Reports and graphs are available in:", OUTPUT_FOLDER)

import pandas as pd
import os

folder = "Data"

files = [
    "patients.csv",
    "encounters.csv",
    "observations.csv",
    "conditions.csv",
    "medications.csv"
]

for file in files:
    path = os.path.join(folder, file)

    if os.path.exists(path):
        df = pd.read_csv(path)

        print("\n========================")
        print("FILE:", file)
        print("========================")

        print("Total rows:", len(df))
        print("Exact duplicate rows:", df.duplicated().sum())

        duplicates = df[df.duplicated(keep=False)]

        print("\nDuplicate records:")
        print(duplicates.head(10))

        # Check duplicate IDs if an ID column exists
        if "Id" in df.columns:
            print("\nDuplicate IDs:", df["Id"].duplicated().sum())



# =====================================
# STEP 2: DATA CLEANING
# =====================================

clean_folder = "Cleaned_Data"
os.makedirs(clean_folder, exist_ok=True)

print("\n========== DATA CLEANING ==========")

for file in files:

    path = os.path.join(folder, file)

    if not os.path.exists(path):
        continue

    df = pd.read_csv(path)

    original_rows = len(df)

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    removed_rows = original_rows - len(df)

    # Convert date columns into datetime format
    for col in df.columns:
        if col.upper() in ["BIRTHDATE", "DEATHDATE",
                           "START", "STOP", "DATE"]:
            df[col] = pd.to_datetime(
                df[col], errors="coerce", utc=True
            )

    # Save cleaned dataset separately
    output_path = os.path.join(clean_folder, file)
    df.to_csv(output_path, index=False)

    print("\nFile:", file)
    print("Original Rows:", original_rows)
    print("Duplicates Removed:", removed_rows)
    print("Cleaned Rows:", len(df))
    print("Saved:", output_path)

print("\nData Cleaning Completed!")


import pandas as pd
import os

folder = "Cleaned_Data"
output_folder = "Outputs"

os.makedirs(output_folder, exist_ok=True)

report = []

for file in os.listdir(folder):

    if file.endswith(".csv"):

        path = os.path.join(folder, file)
        df = pd.read_csv(path)

        print("\n==========================")
        print("FILE:", file)
        print("==========================")

        for column in df.columns:

            missing_count = df[column].isnull().sum()

            missing_percentage = (
                missing_count / len(df)
            ) * 100

            print(
                column,
                "Missing:",
                missing_count,
                "Percentage:",
                round(missing_percentage, 2),
                "%"
            )

            report.append({
                "File": file,
                "Column": column,
                "Missing_Count": missing_count,
                "Missing_Percentage": round(
                    missing_percentage, 2
                )
            })

report_df = pd.DataFrame(report)

report_df.to_csv(
    os.path.join(output_folder, "missing_values_report.csv"),
    index=False
)

print("\nMissing Values Analysis Completed!")
print("Report saved in Outputs folder.")



# ==========================================
# DATA TYPE CONVERSION AND VALIDATION
# ==========================================

import pandas as pd
import os

input_folder = "Cleaned_Data"
output_folder = "Preprocessed_Data"

os.makedirs(output_folder, exist_ok=True)

date_columns = {
    "patients.csv": ["BIRTHDATE", "DEATHDATE"],
    "encounters.csv": ["START", "STOP"],
    "observations.csv": ["DATE"],
    "conditions.csv": ["START", "STOP"],
    "medications.csv": ["START", "STOP"]
}

for file, columns in date_columns.items():

    path = os.path.join(input_folder, file)

    if not os.path.exists(path):
        print(file, "NOT FOUND")
        continue

    df = pd.read_csv(path)

    print("\n==============================")
    print("FILE:", file)
    print("==============================")

    for column in columns:

        if column in df.columns:

            original_missing = df[column].isnull().sum()

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            converted_missing = df[column].isnull().sum()

            invalid_dates = converted_missing - original_missing

            print("Column:", column)
            print("Missing values:", original_missing)
            print("Invalid dates:", max(0, invalid_dates))

    output_path = os.path.join(output_folder, file)

    df.to_csv(output_path, index=False)

    print("Saved:", output_path)

print("\nDate Conversion and Validation Completed!")


import pandas as pd

patients = pd.read_csv("Cleaned_Data/patients.csv")
observations = pd.read_csv("Cleaned_Data/observations.csv")

print("PATIENTS COLUMNS:")
print(patients.columns.tolist())

print("\nOBSERVATIONS COLUMNS:")
print(observations.columns.tolist())

print("\nOBSERVATION TYPES:")
print(observations["DESCRIPTION"].value_counts().head(15))

# ==========================================
# EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# Select dataset folder
if os.path.exists("Preprocessed_Data/patients.csv"):
    data_folder = "Preprocessed_Data"
else:
    data_folder = "Cleaned_Data"

output_folder = "Outputs"
os.makedirs(output_folder, exist_ok=True)

# Load datasets
patients = pd.read_csv(os.path.join(data_folder, "patients.csv"))
observations = pd.read_csv(os.path.join(data_folder, "observations.csv"))
conditions = pd.read_csv(os.path.join(data_folder, "conditions.csv"))

print("\n========== EDA STARTED ==========")

# 1. Gender Distribution
gender_counts = patients["GENDER"].value_counts()

plt.figure(figsize=(7, 5))
gender_counts.plot(kind="bar")
plt.title("Patient Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Number of Patients")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "eda_gender_distribution.png"))
plt.close()

# 2. Top 10 Common Conditions
top_conditions = conditions["DESCRIPTION"].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_conditions.sort_values().plot(kind="barh")
plt.title("Top 10 Common Health Conditions")
plt.xlabel("Number of Records")
plt.ylabel("Condition")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "eda_top_conditions.png"))
plt.close()

# 3. Observation Type Distribution
observation_counts = observations["DESCRIPTION"].value_counts().head(10)

plt.figure(figsize=(10, 6))
observation_counts.sort_values().plot(kind="barh")
plt.title("Top 10 Health Observations")
plt.xlabel("Number of Records")
plt.ylabel("Observation")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "eda_observation_types.png"))
plt.close()

# 4. Blood Pressure Analysis
bp = observations[
    observations["DESCRIPTION"].isin([
        "Systolic Blood Pressure",
        "Diastolic Blood Pressure"
    ])
].copy()

bp["VALUE"] = pd.to_numeric(bp["VALUE"], errors="coerce")
bp = bp.dropna(subset=["VALUE"])

plt.figure(figsize=(8, 5))

for name, group in bp.groupby("DESCRIPTION"):
    plt.hist(group["VALUE"], bins=30, alpha=0.5, label=name)

plt.title("Blood Pressure Value Distribution")
plt.xlabel("Blood Pressure Value")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "eda_blood_pressure.png"))
plt.close()

# 5. Heart Rate Distribution
heart_rate = observations[
    observations["DESCRIPTION"] == "Heart rate"
].copy()

heart_rate["VALUE"] = pd.to_numeric(
    heart_rate["VALUE"], errors="coerce"
)
heart_rate = heart_rate.dropna(subset=["VALUE"])

plt.figure(figsize=(8, 5))
plt.hist(heart_rate["VALUE"], bins=30)
plt.title("Heart Rate Distribution")
plt.xlabel("Heart Rate")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "eda_heart_rate.png"))
plt.close()

print("\nEDA Completed Successfully!")
print("Graphs saved in Outputs folder.")
print("Number of patients:", len(patients))
print("Number of observations:", len(observations))
print("Number of conditions:", len(conditions))

# =====================================
# M1.1 - DATASET COVERAGE ANALYSIS
# =====================================

import pandas as pd
import os

data_folder = "Preprocessed_Data"

if not os.path.exists(data_folder):
    data_folder = "Cleaned_Data"

patients = pd.read_csv(
    os.path.join(data_folder, "patients.csv")
)

observations = pd.read_csv(
    os.path.join(data_folder, "observations.csv")
)

total_patients = patients["Id"].nunique()

health_parameters = [
    "Systolic Blood Pressure",
    "Diastolic Blood Pressure",
    "Heart rate",
    "Body Mass Index",
    "Body Height",
    "Body Weight"
]

print("\n========== M1 DATASET COVERAGE ==========")

print("Total Patients:", total_patients)

for parameter in health_parameters:

    records = observations[
        observations["DESCRIPTION"] == parameter
    ]

    covered_patients = records["PATIENT"].nunique()

    coverage = (
        covered_patients / total_patients
    ) * 100 if total_patients > 0 else 0

    print("\nParameter:", parameter)
    print("Patients Covered:", covered_patients)
    print("Coverage:", round(coverage, 2), "%")

print("\nCoverage Analysis Completed!")

