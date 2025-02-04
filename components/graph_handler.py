import base64
import logging
from io import BytesIO

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from sklearn.neighbors import NearestNeighbors


class GraphHandler:
    def __init__(self, functions=None, classes=None, embeddings=None, k=2):
        self.functions = functions
        self.classes = classes
        self.embeddings = embeddings
        self.k = k

    def create_graph(self):
        """
        Determines the type of graph to generate:
        - If functions & classes are provided → Generates a Component Graph
        - If embeddings are provided → Generates a k-NN Graph
        """
        if self.functions and self.classes:
            return self._create_component_graph()
        elif self.embeddings:
            return self._create_knn_graph()
        else:
            raise ValueError("Insufficient data to generate a graph.")

    def _create_component_graph(self):
        """
        Create a component graph where classes, functions, and files are nodes.
        Relationships between them are edges.
        """
        G = nx.DiGraph()  # ✅ Use Directed Graph for execution flow

        # Add nodes for files and link them to classes and functions
        for file_name, func_name, _ in self.functions:
            G.add_node(func_name, type='function')
            G.add_edge(file_name, func_name)

        for file_name, class_name, _ in self.classes:
            G.add_node(class_name, type='class')
            G.add_edge(file_name, class_name)

        # Add edges between classes and functions they call
        for file_name, func_name, _ in self.functions:
            for file_name2, class_name, _ in self.classes:
                G.add_edge(class_name, func_name)

        return G

    def visualize_graph(self, G):
        """
        Visualize the k-NN graph or component graph using Matplotlib and NetworkX.
        Returns the image as a BytesIO object for Flask to send as a response.
        """
        plt.figure(figsize=(6, 6))

        # Define the node colors based on their type
        node_color_map = {
            'function': 'skyblue',
            'class': 'lightgreen',
            'file': 'lightgray'
        }

        # Positioning nodes using spring layout
        pos = nx.spring_layout(G, seed=42, k=0.2, iterations=30)  # Adjust layout for better visibility

        # Set node colors based on their type (function, class, etc.)
        node_colors = [
            node_color_map.get(G.nodes[node].get('type', 'file'), 'lightgray') for node in G.nodes
        ]

        # Draw nodes and labels
        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=node_colors, edgecolors='black')
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_color="black")

        # ✅ Draw directed edges with arrows
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, width=1.5)

        # Add a title and display the plot
        plt.title("Generated Graph: Repository Structure", fontsize=16)

        # Save the plot to a BytesIO object
        img_stream = BytesIO()
        plt.savefig(img_stream, format='PNG')
        img_stream.seek(0)  # Rewind the BytesIO object to the beginning
        plt.close()  # Close the plot to avoid it from showing in the console

        return img_stream  # Return the BytesIO stream for Flask API response

    def get_representative_files(self, G, top_n=5):
        """
        Identifies the most representative files in a component graph.

        Parameters:
        - G (networkx.Graph): The Component Graph of the repository.
        - top_n (int): Number of top representative files to select.

        Returns:
        - List[str]: Names of the most representative files.
        """
        try:
            if not isinstance(G, nx.Graph) and not isinstance(G, nx.DiGraph):
                raise TypeError("Expected a NetworkX Graph object, but received something else.")

            # Compute centrality scores
            degree_centrality = nx.degree_centrality(G)
            betweenness_centrality = nx.betweenness_centrality(G)

            # Combine centrality scores
            combined_centrality = {
                node: degree_centrality[node] + betweenness_centrality[node]
                for node in G.nodes
            }

            # Sort files by importance (descending)
            sorted_files = sorted(combined_centrality, key=combined_centrality.get, reverse=True)

            # Select top N representative files
            representative_files = sorted_files[:top_n]

            logging.info(f"Representative Files Selected: {representative_files}")

            return representative_files
        except Exception as e:
            logging.error(f"Error selecting representative files: {str(e)}")
            return []

    def _create_knn_graph(self):
        """Creates a k-NN graph using the embeddings dictionary {filename: embedding}."""
        if not self.embeddings:
            raise ValueError("No embeddings provided for k-NN graph.")

        # ✅ Convert dictionary to list
        file_names = list(self.embeddings.keys())
        embeddings_matrix = np.array(list(self.embeddings.values()))

        # ✅ Perform k-NN search
        nbrs = NearestNeighbors(n_neighbors=min(self.k + 1, len(file_names)), algorithm="ball_tree").fit(
            embeddings_matrix)
        distances, indices = nbrs.kneighbors(embeddings_matrix)

        # ✅ Construct the k-NN graph
        G = nx.DiGraph()
        for idx, file_name in enumerate(file_names):
            G.add_node(file_name)  # Use file name as node label

            for neighbor_idx in indices[idx][1:]:  # Skip self (first index)
                neighbor_name = file_names[neighbor_idx]
                G.add_edge(file_name, neighbor_name, weight=distances[idx][1])

        return G