import base64
from io import BytesIO

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


class GraphHandler:
    def __init__(self, functions, classes):
        self.functions = functions
        self.classes = classes

    def create_component_graph(self):
        """
        Create a component graph where classes, functions, and files are nodes.
        Relationships between them are edges.
        """
        G = nx.DiGraph()

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

    def create_knn_graph(self, embeddings, k=3):
        G = nx.Graph()

        # Add nodes to the graph (each node is a code file)
        for idx, (file_name, embedding) in enumerate(embeddings):
            # print(file_name, embedding)
            G.add_node(idx, file_name=file_name, embedding=embedding)

        # Add edges based on similarity between file embeddings (Cosine similarity)
        for i, (file_name_i, embedding_i) in enumerate(embeddings):
            similarities = []
            for j, (file_name_j, embedding_j) in enumerate(embeddings):
                if i != j:
                    similarity = np.dot(embedding_i, embedding_j) / (
                                np.linalg.norm(embedding_i) * np.linalg.norm(embedding_j))  # Cosine similarity
                    similarities.append((j, similarity))

            # Sort by similarity and keep the top K neighbors
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_k_neighbors = similarities[:k]

            for neighbor_idx, similarity in top_k_neighbors:
                G.add_edge(i, neighbor_idx, weight=similarity)

        return G

    def visualize_graph(self, G):
        """
        Visualize the component graph using Matplotlib and NetworkX.
        Returns the image as a BytesIO object for Flask to send as a response.
        """
        plt.figure(figsize=(8, 8))

        # Define the node colors based on their type
        node_color_map = {
            'function': 'skyblue',
            'class': 'lightgreen',
            'file': 'lightgray'
        }

        # Positioning nodes using spring layout
        pos = nx.spring_layout(G, seed=42, k=0.15, iterations=20)  # Adjusting parameters for a better layout

        # Set node colors based on their type (function, class, etc.)
        node_colors = [
            node_color_map[G.nodes[node].get('type', 'file')] for node in G.nodes
        ]

        # Draw the graph with customized aesthetics
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=3000,
            node_color=node_colors,
            font_weight='bold',
            font_size=12,
            edge_color='gray',
            width=1.5,
            arrows=True,
            font_color='black',
            edgecolors='black'
        )

        # Add a title and display the plot
        plt.title("Component Graph: Repo Design and Relationships", fontsize=16)

        # Save the plot to a BytesIO object
        img_stream = BytesIO()
        plt.savefig(img_stream, format='PNG')
        img_stream.seek(0)  # Rewind the BytesIO object to the beginning
        plt.close()  # Close the plot to avoid it from showing in the console

        # Return the BytesIO stream to be sent as a file response
        return img_stream
