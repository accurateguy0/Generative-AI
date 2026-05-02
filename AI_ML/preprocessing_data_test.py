import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler

# Create a dummy dataset
np.random.seed(0)
dummy_data = {
    'Feature1': np.random.normal(100, 10, 100).tolist() + [np.nan, 200],  # Normally distributed with an outlier
    'Feature2': np.random.randint(0, 100, 102).tolist(),  # Random integers
    'Category': ['A', 'B', 'C', 'D'] * 25 + [np.nan, 'A'],  # Categorical with some missing values
    'Target': np.random.choice([0, 1], 102).tolist()  # Binary target variable
}

# Convert the dictionary to a pandas DataFrame
df_dummy = pd.DataFrame(dummy_data)

# Display the first few rows of the dummy dataset
print(df_dummy.head())

def load_data(df):
    return df

def handle_missing_values(df):
    # Added numeric_only=True to prevent errors with text columns
    return df.fillna(df.mean(numeric_only=True))

def remove_outliers(df):
    # Calculate Z-scores only for numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    z_scores = np.abs(stats.zscore(numeric_df))
    # Filter original dataframe based on numeric z-scores
    return df[(z_scores < 3).all(axis=1)]

def scale_data(df):
    scaler = StandardScaler()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if not numeric_cols.empty:
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

def encode_categorical(df, categorical_columns):
    # Verify columns exist before encoding to avoid errors
    existing_cols = [col for col in categorical_columns if col in df.columns]
    return pd.get_dummies(df, columns=existing_cols)

def save_data(df, output_filepath):
    df.to_csv(output_filepath, index=False)

# Load the data
df_preprocessed = load_data(df_dummy)

# Handle missing values
df_preprocessed = handle_missing_values(df_preprocessed)

# Remove outliers
df_preprocessed = remove_outliers(df_preprocessed)

# Scale the data
df_preprocessed = scale_data(df_preprocessed)

# Encode categorical variables
df_preprocessed = encode_categorical(df_preprocessed, ['Category'])

# Display the preprocessed data
print("--- Preprocessed Data Head ---")
print(df_preprocessed.head())

# Save the cleaned and preprocessed DataFrame to a CSV file
save_data(df_preprocessed, 'preprocessed_dummy_data.csv')

print('\nPreprocessing complete. Preprocessed data saved as preprocessed_dummy_data.csv')

# Check for missing values: 
print("\n--- Missing Values Check ---")
print(df_preprocessed.isnull().sum())

# Verify outlier removal:
print("\n--- Statistics Summary (Check for Outliers) ---")
print(df_preprocessed.describe())

# Inspect scaled data: 
print("\n--- Final Head Inspection ---")
print(df_preprocessed.head())

# Check categorical encoding:
print("\n--- Final Column List ---")
print(df_preprocessed.columns)
