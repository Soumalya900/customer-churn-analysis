# Import required libraries
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# -------------------------------
# 1. Load Dataset
# -------------------------------
# Read the dataset from CSV file
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "..", "data", "02_final_featured_data.csv")
data = pd.read_csv(file_path)

# -------------------------------
# 2. Stratified Train-Test Split
# -------------------------------
# Ensures same churn distribution in train and test sets
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_index, test_index in split.split(data, data["Churn"]):
    strat_train_set = data.loc[train_index]
    strat_test_set = data.loc[test_index]

# Separate features and target variable
X_train = strat_train_set.drop(["customerID", "Churn"], axis=1)
y_train = strat_train_set["Churn"]

X_test = strat_test_set.drop(["customerID", "Churn"], axis=1)
y_test = strat_test_set["Churn"]

# -------------------------------
# 3. Data Preprocessing
# -------------------------------
# Convert categorical variables into numeric using One-Hot Encoding
X_train = pd.get_dummies(X_train)
X_test = pd.get_dummies(X_test)

# Align test set columns with training set (important step)
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

# -------------------------------
# 4. Model Training
# -------------------------------
# Initialize Random Forest model with tuned parameters
model = RandomForestClassifier(
    n_estimators=1000,          # Number of trees
    max_depth=10,               # Limit depth to avoid overfitting
    min_samples_split=5,        # Minimum samples required to split
    class_weight='balanced',    # Handle class imbalance
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# -------------------------------
# 5. Prediction & Evaluation
# -------------------------------
# Predict churn probability for test set
probs = model.predict_proba(X_test)[:, 1]

# Apply custom threshold (0.3 instead of default 0.5)
threshold = 0.3
preds = (probs > threshold).astype(int)

# Print evaluation metrics
print(f"Threshold: {threshold}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, preds))

print("\nClassification Report:")
print(classification_report(y_test, preds))

# -------------------------------
# 6. Feature Importance Analysis
# -------------------------------
# Extract feature importance scores from model
importances = model.feature_importances_
feature_names = X_train.columns

# Create DataFrame for better visualization
feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
})

# Sort and select top 10 important features
feature_importance_df = feature_importance_df.sort_values(
    by='Importance', ascending=False
).head(10)

# -------------------------------
# 7. Visualization
# -------------------------------
# Plot top 10 churn drivers
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.title("Top 10 Drivers of Customer Churn")
plt.gca().invert_yaxis()  # Highest importance on top
plt.show()

# -------------------------------
# 8. Save Output
# -------------------------------
# Save feature importance to CSV (for Power BI dashboard)
feature_importance_df.to_csv("feature_importance.csv", index=False)