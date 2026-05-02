import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy import stats
import missingno as msno  # Optional: for visualizing missing data
import matplotlib.pyplot as plt

# 1. Load your dataset
# Replace 'your_dataset.csv' with your actual file name
try:
    df = pd.read_csv('your_dataset.csv')
    print("Dataset loaded successfully. First 5 rows:")
    print(df.head())
except FileNotFoundError:
    print("Error: 'your_dataset.csv' not found.")
    exit()

# 2. Handle missing values
# Option 1: Drop rows with missing values
df_cleaned = df.dropna().copy()

# Option 2: Fill missing values with the mean (numeric only)
df_filled = df.fillna(df.mean(numeric_only=True))

# 3. Visualize missing data (optional - requires matplotlib)
# msno.matrix(df)
# plt.show()

# 4. Identify outliers using Z-score (Numeric columns only)
numeric_df = df_cleaned.select_dtypes(include=[np.number])
if not numeric_df.empty:
    z_scores = np.abs(stats.zscore(numeric_df))
    # Keep rows where all numeric columns have a Z-score < 3
    df_no_outliers = df_cleaned[(z_scores < 3).all(axis=1)].copy()
else:
    df_no_outliers = df_cleaned.copy()

# 5. Cap outliers (Manual Example)
# Change 'column_name' to a real numeric column in your file
target_col = 'column_name'
if target_col in df_no_outliers.columns:
    upper_limit = df_no_outliers[target_col].quantile(0.95)
    df_no_outliers[target_col] = np.where(df_no_outliers[target_col] > upper_limit, upper_limit, df_no_outliers[target_col])

# 6. Scaling (Numeric columns only)
if not numeric_df.empty:
    scaler_minmax = MinMaxScaler()
    # Apply Min-Max scaling to numeric columns
    df_scaled = df_no_outliers.copy()
    df_scaled[numeric_df.columns] = scaler_minmax.fit_transform(df_no_outliers[numeric_df.columns])
    
    scaler_std = StandardScaler()
    # Apply Standard scaling
    df_standardized = df_no_outliers.copy()
    df_standardized[numeric_df.columns] = scaler_std.fit_transform(df_no_outliers[numeric_df.columns])
else:
    df_scaled = df_no_outliers
    df_standardized = df_no_outliers

# 7. One-hot encoding for categorical variables
# Change 'categorical_column_name' to a real text column in your file
cat_col = 'categorical_column_name'
if cat_col in df_scaled.columns:
    df_encoded = pd.get_dummies(df_scaled, columns=[cat_col])
else:
    df_encoded = df_scaled

# 8. Save the final result
df_encoded.to_csv('cleaned_preprocessed_data.csv', index=False)
print('Data cleaning and preprocessing complete. File saved as cleaned_preprocessed_data.csv')
