import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy import stats
import missingno as msno  # Optional: for visualizing missing data
import matplotlib.pyplot as plt

# 1. Load your dataset
# IMPORTANT: Replace 'your_dataset.csv' with your actual filename (e.g., 'scraped_data.csv')
try:
    df = pd.read_csv('your_dataset.csv')
    print("Dataset loaded successfully.")
    print(df.head())
except FileNotFoundError:
    print("Error: File 'your_dataset.csv' not found. Please check the filename.")
    exit()

# 2. Visualize missing data (optional)
# Note: These require a display environment to show up
msno.matrix(df)
plt.show()

# 3. Handle Missing Values
# Option A: Drop rows with missing values
df_cleaned = df.dropna().copy()

# Option B: Fill missing values with the mean (only for numeric columns)
df_filled = df.fillna(df.mean(numeric_only=True))

# 4. Identify and remove outliers using Z-score
# We only calculate Z-score on numeric columns to avoid errors
numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
z_scores = np.abs(stats.zscore(df_cleaned[numeric_cols]))

# Keep rows where all numeric columns have a Z-score less than 3
df_no_outliers = df_cleaned[(z_scores < 3).all(axis=1)].copy()

# 5. Cap outliers at a threshold (Example for a specific column)
# Replace 'column_name' with a real column name from your CSV
target_col = 'column_name' 
if target_col in df_no_outliers.columns:
    upper_limit = df_no_outliers[target_col].quantile(0.95)
    df_no_outliers[target_col] = np.where(df_no_outliers[target_col] > upper_limit, upper_limit, df_no_outliers[target_col])

# 6. Scaling (on numeric columns only)
scaler_minmax = MinMaxScaler()
scaler_std = StandardScaler()

# Scaling only the numeric data
df_numeric = df_no_outliers[numeric_cols]

df_scaled = pd.DataFrame(scaler_minmax.fit_transform(df_numeric), columns=numeric_cols)
df_standardized = pd.DataFrame(scaler_std.fit_transform(df_numeric), columns=numeric_cols)

# 7. One-hot encoding for categorical variables
# Replace 'categorical_column_name' with a real column name like 'Sector' or 'Provider'
cat_col = 'categorical_column_name'
if cat_col in df_no_outliers.columns:
    df_encoded = pd.get_dummies(df_no_outliers, columns=[cat_col])
else:
    df_encoded = df_no_outliers

# 8. Save the final result
df_encoded.to_csv('cleaned_preprocessed_data.csv', index=False)
print('Data cleaning complete. Saved as: cleaned_preprocessed_data.csv')
