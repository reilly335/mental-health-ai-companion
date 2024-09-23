# data/scripts/upload_data.py

import os
from seekrflow import SeekrFlowClient

def upload_dataset():
    api_key = os.environ.get('SEEKR_FLOW_API_KEY')
    if not api_key:
        print("Error: SEEKR_FLOW_API_KEY environment variable not set.")
        exit(1)
    
    client = SeekrFlowClient(api_key=api_key)
    
    dataset_path = os.path.join('data', 'processed', 'training_data.parquet')
    dataset_name = 'MH-AI Training Data'
    dataset_description = 'Processed training data for MH-AI fine-tuning.'
    
    dataset_id = client.upload_dataset(
        file_path=dataset_path,
        name=dataset_name,
        description=dataset_description
    )
    
    print(f"Dataset uploaded successfully. Dataset ID: {dataset_id}")

if __name__ == '__main__':
    upload_dataset()
