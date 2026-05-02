import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1. Load the dataset
# Replace 'your_dataset.csv' with your actual file path
try:
    df = pd.read_csv('your_dataset.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'your_dataset.csv' not found.")
    exit()

# 2. Initial Inspection
print("\n--- First 5 Rows ---")
print(df.head())
print("\n--- Data Types ---")
print(df.dtypes)

# 3. Check for missing values
missing_values = df.isnull().sum()
print("\n--- Missing Values Per Column ---")
print(missing_values[missing_values > 0])

# Clean missing values
df_cleaned = df.dropna()  # Option: Drops rows with any missing values
df_filled = df.fillna(df.mean(numeric_only=True))  # Option: Fill numeric with mean

# 4. Outlier Detection
print("\n--- Descriptive Statistics ---")
print(df.describe())

# Boxplot Visualization
# Change 'Column1', 'Column2' to your actual column names
cols_to_plot = [col for col in ['Column1', 'Column2'] if col in df.columns]
if cols_to_plot:
    df.boxplot(column=cols_to_plot)
    plt.title("Boxplot for Outlier Detection")
    plt.show()

# Calculate Z-scores for numeric columns
numeric_df = df.select_dtypes(include=[np.number])
if not numeric_df.empty:
    z_scores = np.abs(stats.zscore(numeric_df))
    # Find rows where ANY numeric column has a Z-score > 3
    outlier_mask = (z_scores > 3).any(axis=1)
    print(f"\nFound {sum(outlier_mask)} rows with outliers.")
    
    # Remove outliers
    df_no_outliers = df[~outlier_mask]
    
    # Transform outliers (Capping)
    # Define upper_limit before using it
    if 'Column1' in df.columns:
        upper_limit = df['Column1'].quantile(0.95)
        df['Column1'] = np.where(df['Column1'] > upper_limit, upper_limit, df['Column1'])

# 5. Categorical Consistency
cat_col = 'CategoryColumn'  # Replace with actual name
if cat_col in df.columns:
    print(f"\n--- Unique values in {cat_col} ---")
    print(df[cat_col].unique())
    print(df[cat_col].value_counts())
    
    # Standardize categories
    df[cat_col] = df[cat_col].astype(str).str.strip().str.lower().replace({'misspelled': 'correct'})

# 6. Numeric Error Correction (Example: Age)
if 'Age' in df.columns:
    print("\n--- Checking for negative ages ---")
    print(df[df['Age'] < 0])
    # Replace negative ages with NaN
    df['Age'] = np.where(df['Age'] < 0, np.nan, df['Age'])

# 7. Cross-Validation
# Example: Part1 + Part2 should equal Total
if all(col in df.columns for col in ['Part1', 'Part2', 'ExpectedTotal']):
    df['Total_Calculated'] = df['Part1'] + df['Part2']
    inconsistent_rows = df[df['Total_Calculated'] != df['ExpectedTotal']]
    print("\n--- Inconsistent Calculation Rows ---")
    print(inconsistent_rows)

# 8. Handle Duplicates
duplicates = df.duplicated().sum()
print(f"\nDuplicate rows found: {duplicates}")
df_no_duplicates = df.drop_duplicates()

# 9. Final Save
df_no_duplicates.to_csv('cleaned_data.csv', index=False)
print("\nCleaning complete. Saved to 'cleaned_data.csv'.")