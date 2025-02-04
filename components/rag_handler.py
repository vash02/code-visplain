import logging
import os

import ollama
import networkx as nx
import graphviz

import config
from components.graph_handler import GraphHandler
from components.summarizer import CodeSummarizer
from components.llm_handler import LLMHandler


class RAGHandler:
    def __init__(self, embedding_generator):
        """
        Initializes the RAGHandler with the embedding generator and summarizer.
        """
        self.embedding_generator = embedding_generator
        self.llm_handler = LLMHandler()  # ✅ Use a dedicated LLM handler
        self.summarizer = CodeSummarizer(self.llm_handler)  # ✅ Integrate summarization

    def generate_sequential_summary(self, repo):
        """
        Generates a **file-based** repository summary and a structured block diagram.
        """
        try:
            logging.info("Fetching functions, classes, and metadata from repository...")
            functions, classes, metadata = repo.fetch_files_from_directory()

            # ✅ Generate Component Graph
            logging.info("Creating component graph...")
            graph_handler = GraphHandler(functions, classes)
            component_graph = graph_handler.create_graph()

            # ✅ Extract only Python file nodes
            file_nodes = [node for node in component_graph.nodes if node.endswith(".py")]

            # ✅ Perform topological sort to get execution order
            logging.info("Performing topological sort to determine execution order...")
            execution_order = list(nx.topological_sort(component_graph.subgraph(file_nodes)))

            if not execution_order:
                logging.error("Execution order is empty. Unable to generate block diagram.")
                return {"error": "Execution order is empty."}

            logging.info(f"Execution Order: {execution_order}")

            # ✅ Group functions by file
            file_function_map = {}
            for file_name, func_name, func_code in functions:
                if file_name not in file_function_map:
                    file_function_map[file_name] = []
                file_function_map[file_name].append((func_name, func_code))

            # ✅ Generate summaries **per file**
            file_summaries = {}
            for file_name, functions in file_function_map.items():
                function_texts = "\n\n".join(
                    [f"Function: {func_name}\n```python\n{func_code}\n```" for func_name, func_code in functions]
                )

                summary_prompt = f"""
                You are an AI expert in Python code analysis. 
                Summarize the following Python file with its key functions concisely:

                **File Name**: {file_name}
                **Functions**:
                {function_texts}

                Provide a structured summary explaining the overall purpose of this file, its key components, 
                and any important parameters with values.
                """

                logging.info(f"Summarizing file: {file_name}")
                response = ollama.chat(model=config.LLM_MODEL_NAME,
                                       messages=[{"role": "user", "content": summary_prompt}])
                file_summary = response["message"]["content"]

                file_summaries[file_name] = file_summary

            # ✅ Generate Block Diagram Using Summaries
            logging.info("Generating block diagram...")
            diagram_path = self.create_block_diagram(execution_order, file_summaries)

            return {
                "file_summaries": file_summaries,
                "pipeline_diagram": diagram_path
            }

        except Exception as e:
            logging.error(f"Error generating sequential summary: {str(e)}")
            return {"error": f"Error processing sequential summary: {str(e)}"}

    def create_block_diagram(self, execution_order, summaries):
        """
        Creates a structured block diagram with main component files and execution order.
        """
        diagram = graphviz.Digraph(format="png")
        diagram.attr(rankdir="LR", bgcolor="white", style="filled", fillcolor="lightgray")

        for file_name in execution_order:
            if file_name not in summaries:  # Skip if not in summary
                continue

            summary = summaries.get(file_name, "No summary available")
            # label_text = f"{file_name}\n{summary[:100]}..."  # Trim long summaries

            diagram.node(file_name, shape="box", style="filled", fillcolor="lightblue")

        for i in range(len(execution_order) - 1):
            diagram.edge(execution_order[i], execution_order[i + 1])

        # Save the diagram
        diagram_path = os.path.join("static", "block_diagram")
        diagram.render(diagram_path)
        logging.info(f"Block diagram saved at {diagram_path}.png")

        return f"/static/block_diagram.png"
