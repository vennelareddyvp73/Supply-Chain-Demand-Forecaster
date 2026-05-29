import os
import logging
import pandas as pd

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def preprocess_data():
    """
    Loads train, test, and store datasets, merges train and test with store on key 'Store',
    and saves the merged files to the processed directory.
    """
    base_data_path = "data/extracted_data"
    if not os.path.exists(os.path.join(base_data_path, "train.csv")):
        base_data_path = "src/data/extracted_data"

    output_data_path = "src/data/processed_data"

    os.makedirs(output_data_path, exist_ok=True)

    logging.info(f"Loading datasets from {base_data_path}...")
    train_df = pd.read_csv(f"{base_data_path}/train.csv", low_memory=False)
    test_df = pd.read_csv(f"{base_data_path}/test.csv", low_memory=False)
    store_df = pd.read_csv(f"{base_data_path}/store.csv", low_memory=False)

    logging.info("Merging train data with store data...")
    train_merged = pd.merge(train_df, store_df, on="Store", how="left")
    train_merged_path = os.path.abspath(f"{output_data_path}/merged_train.csv")
    train_merged.to_csv(train_merged_path, index=False)
    logging.info(f"Merged train data saved to absolute path: {train_merged_path}")

    logging.info("Merging test data with store data...")
    test_merged = pd.merge(test_df, store_df, on="Store", how="left")
    test_merged_path = os.path.abspath(f"{output_data_path}/merged_test.csv")
    test_merged.to_csv(test_merged_path, index=False)
    logging.info(f"Merged test data saved to absolute path: {test_merged_path}")


if __name__ == "__main__":
    preprocess_data()
