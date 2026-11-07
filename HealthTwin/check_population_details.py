import pandas as pd

df = pd.read_csv("Data/patients.csv")

print("Total Patients:", len(df))

print("\nGender Distribution:")
print(df["GENDER"].value_counts(dropna=False))

print("\nState Distribution:")
print(df["STATE"].value_counts(dropna=False))

print("\nCity Distribution:")
print(df["CITY"].value_counts(dropna=False))

print("\nBirth Date Range:")
print("Earliest:", df["BIRTHDATE"].min())
print("Latest:", df["BIRTHDATE"].max())

print("\nSample Patient Locations:")
print(df[["CITY", "STATE", "ZIP"]].head(10))