import pandas as pd

# Load dataset
df = pd.read_csv('data/raw_data.csv')

# Convert TotalCharges to numeric
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Check dataset info
print(df.head())
print(df.info())

# Remove rows with missing TotalCharges
df.dropna(subset=['TotalCharges'], inplace=True)

# Convert SeniorCitizen values
df['SeniorCitizen'] = df['SeniorCitizen'].replace({0: "No", 1: "Yes"})

# Convert Churn values
df['Churn'] = df['Churn'].replace({"Yes": 1, "No": 0})

# Save cleaned dataset
df.to_csv('data/cleaned_churn_data.csv', index=False)