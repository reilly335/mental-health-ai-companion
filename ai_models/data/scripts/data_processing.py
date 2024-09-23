# data/scripts/data_preprocessing.py

import pandas as pd
import json
import os

def load_raw_data():
    # Load data from raw datasets
    data_frames = []
    raw_data_dir = os.path.join('data', 'raw')
    for file_name in os.listdir(raw_data_dir):
        file_path = os.path.join(raw_data_dir, file_name)
        if file_name.endswith('.csv'):
            df = pd.read_csv(file_path)
            data_frames.append(df)
        elif file_name.endswith('.json'):
            df = pd.read_json(file_path, lines=True)
            data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)

def preprocess_data(df):
    # Basic preprocessing steps
    # Remove null values
    df = df.dropna(subset=['prompt', 'response'])
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['prompt', 'response'])
    
    # Text normalization (e.g., lowercasing)
    df['prompt'] = df['prompt'].str.lower()
    df['response'] = df['response'].str.lower()
    
    # Additional preprocessing as needed
    return df

def save_processed_data(df):
    # Save processed data in Parquet format
    processed_data_dir = os.path.join('data', 'processed')
    os.makedirs(processed_data_dir, exist_ok=True)
    output_path = os.path.join(processed_data_dir, 'training_data.parquet')
    df.to_parquet(output_path, index=False)
    print(f"Processed data saved to {output_path}")

def main():
    df = load_raw_data()
    df = preprocess_data(df)
    save_processed_data(df)

if __name__ == '__main__':
    main()
