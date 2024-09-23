# data/scripts/data_preprocessing.py

"""
Data Preprocessing Script for the Mental Health AI Companion

This script performs the following tasks:
- Loads raw data from the 'data/raw/' directory.
- Preprocesses the data (cleaning, normalization, etc.).
- Splits the data into training, validation, and test sets.
- Saves the processed datasets in Parquet format in the 'data/processed/' directory.

Author: Your Name
Date: YYYY-MM-DD
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split

def load_raw_data():
    """
    Load raw data files from the 'data/raw/' directory and concatenate them into a single DataFrame.
    Supported file formats: CSV, JSONL (JSON Lines).

    Returns:
        pd.DataFrame: Combined DataFrame containing all raw data.
    """
    data_frames = []
    raw_data_dir = os.path.join('data', 'raw')
    for file_name in os.listdir(raw_data_dir):
        file_path = os.path.join(raw_data_dir, file_name)
        if file_name.endswith('.csv'):
            print(f"Loading CSV file: {file_name}")
            df = pd.read_csv(file_path)
            data_frames.append(df)
        elif file_name.endswith('.json') or file_name.endswith('.jsonl'):
            print(f"Loading JSON file: {file_name}")
            df = pd.read_json(file_path, lines=True)
            data_frames.append(df)
        else:
            print(f"Unsupported file format: {file_name}. Skipping.")
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        print("Raw data loaded successfully.")
        return combined_df
    else:
        print("No raw data files found.")
        return pd.DataFrame()


def preprocess_data(df):
    """
    Preprocess the data:
    - Remove null or missing values.
    - Remove duplicates.
    - Normalize text (e.g., lowercasing).
    - Additional preprocessing steps as needed.

    Args:
        df (pd.DataFrame): The raw data DataFrame.

    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """
    # Ensure required columns are present
    required_columns = ['prompt', 'response']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        exit(1)

    print("Starting data preprocessing...")

    # Remove null or missing values
    df = df.dropna(subset=required_columns)
    print("Null values removed.")

    # Remove duplicates
    df = df.drop_duplicates(subset=required_columns)
    print("Duplicates removed.")

    # Text normalization
    df['prompt'] = df['prompt'].astype(str).str.strip().str.lower()
    df['response'] = df['response'].astype(str).str.strip().str.lower()
    print("Text normalization completed.")

    # Additional preprocessing steps can be added here
    # For example: removing special characters, lemmatization, etc.

    print("Data preprocessing completed.")
    return df

def split_data(df):
    """
    Split the DataFrame into training, validation, and test sets.

    Args:
        df (pd.DataFrame): The preprocessed DataFrame.

    Returns:
        tuple: (train_df, val_df, test_df)
    """
    print("Splitting data into training, validation, and test sets...")
    train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)
    print(f"Training set size: {len(train_df)}")
    print(f"Validation set size: {len(val_df)}")
    print(f"Test set size: {len(test_df)}")
    return train_df, val_df, test_df

def save_processed_data(train_df, val_df, test_df):
    """
    Save the processed datasets in Parquet format in the 'data/processed/' directory.

    Args:
        train_df (pd.DataFrame): Training dataset.
        val_df (pd.DataFrame): Validation dataset.
        test_df (pd.DataFrame): Test dataset.
    """
    processed_data_dir = os.path.join('data', 'processed')
    os.makedirs(processed_data_dir, exist_ok=True)

    train_path = os.path.join(processed_data_dir, 'training_data.parquet')
    val_path = os.path.join(processed_data_dir, 'validation_data.parquet')
    test_path = os.path.join(processed_data_dir, 'test_data.parquet')

    train_df.to_parquet(train_path, index=False)
    val_df.to_parquet(val_path, index=False)
    test_df.to_parquet(test_path, index=False)

    print("Processed data saved successfully:")
    print(f"- Training data: {train_path}")
    print(f"- Validation data: {val_path}")
    print(f"- Test data: {test_path}")

def main():
    # Load raw data
    df = load_raw_data()
    if df.empty:
        print("No data to process. Exiting.")
        exit(1)

    # Preprocess data
    df = preprocess_data(df)

    # Split data
    train_df, val_df, test_df = split_data(df)

    # Save processed data
    save_processed_data(train_df, val_df, test_df)

    print("Data preprocessing pipeline completed successfully.")

if __name__ == '__main__':
    main()
