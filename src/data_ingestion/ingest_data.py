import os
import zipfile
from abc import ABC, abstractmethod

import pandas as pd

class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame | dict[str, pd.DataFrame]:
        pass


class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame | dict[str, pd.DataFrame]:

        if not file_path.endswith(".zip"):
            raise ValueError("The provided file is not a .zip file.")

        parent_dir = os.path.dirname(file_path) or "."
        if os.path.basename(parent_dir) == "raw_data":
            target_dir = os.path.join(os.path.dirname(parent_dir) or ".", "extracted_data")
        else:
            target_dir = os.path.join(parent_dir, "extracted_data")

        # Ensure the data folder is created inside 'src'
        if not target_dir.replace("\\", "/").startswith("src"):
            target_dir = os.path.join("src", target_dir.lstrip(".\\/"))

        os.makedirs(target_dir, exist_ok=True)

        dataframes = {}
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                if member.endswith(".csv"):
                    zip_ref.extract(member, target_dir)
                
                    csv_path = os.path.join(target_dir, member)
                    key = os.path.splitext(member)[0]
                    dataframes[key] = pd.read_csv(csv_path, low_memory=False)

        if len(dataframes) == 0:
            raise FileNotFoundError("No CSV file found in the zip archive.")

        if len(dataframes) == 1:
            return list(dataframes.values())[0]

        return dataframes


class DataIngestorFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestor:
        """Returns the appropriate DataIngestor based on file extension."""
        if file_extension == ".zip":
            return ZipDataIngestor()
        else:
            raise ValueError(f"No ingestor available for file extension: {file_extension}")


# test
if __name__ == "__main__":
    
    file_path = "src/data/raw_data/rossmann-store-sales.zip"
    file_extension = os.path.splitext(file_path)[1]
    data_ingestor = DataIngestorFactory.get_data_ingestor(file_extension)

    result = data_ingestor.ingest(file_path)

    if isinstance(result, dict):
        print("Multiple DataFrames ingested:")
        for name, df in result.items():
            print(f"- {name}: shape={df.shape}")
    else:
        print(f"Single DataFrame ingested: shape={result.shape}")

