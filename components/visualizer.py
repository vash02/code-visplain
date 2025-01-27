import os
from io import BytesIO

import networkx as nx
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self):
        pass

    def visualize_graph(self, G):
        """
        Visualize the component graph using Matplotlib and NetworkX.
        Returns the image as a BytesIO object for Flask to send as a response.
        """
        plt.figure(figsize=(12, 12))

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

    def visualize_kag_insights(self, query):
        pass
