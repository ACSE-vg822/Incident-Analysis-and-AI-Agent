import os
import pandas as pd

class DataLoader:
    """A class to handle loading of dataset."""

    def __init__(self, base_dir=None, file_name="parsed_data/parsed_incident_reports.csv"):
        self.base_dir = base_dir or os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.base_dir, "..", file_name)

    def load_data(self):
        """Load the dataset from a CSV file."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        return pd.read_csv(self.file_path)

class DataPreprocessor:
    """A class to handle preprocessing of dataset."""

    @staticmethod
    def preprocess(data):
        """Preprocess the dataset to extract and format date information."""
        # Ensure Date column is in datetime format
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        # Extract year and month as a string (instead of Period)
        data['YearMonth'] = data['Date'].dt.to_period('M').astype(str)
        return data
