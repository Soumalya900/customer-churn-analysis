import pandas as pd
from pandasql import sqldf

def main():
    
    # 1. Load Cleaned Dataset
    print("Loading cleaned dataset...")
    df = pd.read_csv("cleaned_churn_data.csv")

    # 2. Setup SQL Environment
    pysqldf = lambda q: sqldf(q, globals())

    # 3. Feature Engineering – Tenure Bucketing
    print("Applying tenure bucketing feature...")
    query_tenure = """
    SELECT *,
        CASE 
            WHEN tenure <= 12 THEN '0-1 Year'
            WHEN tenure > 12 AND tenure <= 24 THEN '1-2 Years'
            WHEN tenure > 24 AND tenure <= 48 THEN '2-4 Years'
            WHEN tenure > 48 AND tenure <= 60 THEN '4-5 Years'
            ELSE '5+ Years'
        END AS tenure_group
    FROM df
    """

    df = pysqldf(query_tenure)

    # Preview
    print(df[['customerID', 'tenure', 'tenure_group']].head())

    # 4. Feature Engineering – Total Services
    print("Calculating total services feature...")
    query_services = """
    SELECT *,
        (CASE WHEN OnlineSecurity = 'Yes' THEN 1 ELSE 0 END +
         CASE WHEN OnlineBackup = 'Yes' THEN 1 ELSE 0 END +
         CASE WHEN DeviceProtection = 'Yes' THEN 1 ELSE 0 END +
         CASE WHEN TechSupport = 'Yes' THEN 1 ELSE 0 END +
         CASE WHEN StreamingTV = 'Yes' THEN 1 ELSE 0 END +
         CASE WHEN StreamingMovies = 'Yes' THEN 1 ELSE 0 END) AS total_services
    FROM df
    """

    df = pysqldf(query_services)

    # Preview
    print(df[['customerID', 'total_services', 'Churn']].head())

    # 5. Logic Validation
    print(df.groupby('total_services')['Churn'].mean())

    # 6. Export Final Dataset
    df.to_csv("final_featured_data.csv", index=False)