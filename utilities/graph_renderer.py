import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit as st

class GraphRenderer:
    """A class to handle graph creation, rendering, and Streamlit interface."""

    def __init__(self, data):
        """
        Initialize the GraphRenderer with the dataset.

        Args:
            data (DataFrame): The dataset containing relationships between nodes.
        """
        self.data = data

    def create_graph(self, filtered_data=None):
        """Create a NetworkX graph from the dataset."""
        G = nx.Graph()
        data_to_use = filtered_data if filtered_data is not None else self.data
        for _, row in data_to_use.iterrows():
            G.add_edge(row['Node1'], row['Node2'], weight=row['Incident Count'])
        return G

    def render_graph(self, G):
        """Render the graph using Pyvis and save it as an HTML file."""
        net = Network(notebook=True, height="750px", width="100%", bgcolor="white", font_color="black")
        net.from_nx(G)
        net.show("graph.html")

    def graph_ui(self):
        """Render the Streamlit interface for the graph."""
        #st.title("Interactive Service and Component Correlation Graph")

        # Dropdown for selecting a node to filter
        selected_node = st.selectbox(
            "Select a service/component to highlight (shows related nodes):",
            ['None'] + list(pd.concat([self.data['Node1'], self.data['Node2']]).unique())
        )

        # Filter data based on selected node
        if selected_node and selected_node != 'None':
            filtered_data = self.data[(self.data['Node1'] == selected_node) | (self.data['Node2'] == selected_node)]
        else:
            filtered_data = self.data

        # Create and render graph
        G = self.create_graph(filtered_data)
        self.render_graph(G)

        # Display the graph in Streamlit
        st.components.v1.html(open("graph.html", "r").read(), height=750)
