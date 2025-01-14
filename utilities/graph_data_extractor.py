import pandas as pd

class GraphDataExtractor:
    """A class to handle extraction of graph relationships from the dataset."""

    def __init__(self, data):
        """
        Initialize the GraphDataExtractor with the dataset.

        Args:
            data (DataFrame): The parsed incident dataset.
        """
        self.data = data

    def extract_graph_data(self):
        """
        Extract graph relationships from the dataset.

        Returns:
            DataFrame: A dataframe with 'Node1', 'Node2', and 'Incident Count' columns.
        """
        # Group by Component and Service to count relationships
        graph_data = (
            self.data.groupby(['Component', 'Service'])
            .size()
            .reset_index(name='Incident Count')
            .rename(columns={'Component': 'Node1', 'Service': 'Node2'})
        )
        return graph_data
