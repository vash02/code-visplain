import io
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS  # Enable CORS for frontend
import os
import logging
import matplotlib

from components.llm_handler import LLMHandler
from components.rag_handler import RAGHandler
from components.repository import CodeRepository
from components.analyzer import CodeAnalyzer
from components.graph_handler import GraphHandler
from components.embedding_generator import EmbeddingGenerator
import config
from components.summarizer import CodeSummarizer

matplotlib.use('Agg')  # Use non-GUI backend

STATIC_FOLDER = "static"
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path="/static")
CORS(app)  # Enable CORS

logging.basicConfig(level=logging.DEBUG)

# Initialize components
embedding_generator = EmbeddingGenerator()
code_analyzer = CodeAnalyzer()
repo_token = config.GITHUB_TOKEN

@app.route('/')
def index():
    return send_from_directory('frontend/build', 'index.html')


@app.route('/upload', methods=['POST'])
def upload_code():
    """Handles file upload or repo-based extraction."""
    upload_option = request.form.get('uploadOption')
    logging.debug(f"Upload option selected: {upload_option}")

    if upload_option == 'file':
        file = request.files.get('code_file')
        if not file or file.filename == '':
            return jsonify({"error": "No valid file selected"})

        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        with open(file_path, 'r') as f:
            file_content = f.read()

        return process_code(file_content)

    elif upload_option == 'repo':
        repo_owner = request.form['repo_owner']
        repo_name = request.form['repo_name']
        repo = CodeRepository(repo_owner, repo_name, repo_token)
        return process_code(repo)

    return jsonify({"error": "Invalid input option"})


def process_code(repo):
    """Processes code, generates embeddings, and builds Component Graph."""
    try:
        functions, classes, relations = repo.fetch_files_from_directory()

        # Generate embeddings
        embeddings = embedding_generator.generate_embeddings_batch(repo)

        # Generate Component Graph
        graph_handler = GraphHandler(functions=functions, classes=classes)
        component_graph = graph_handler.create_graph()

        # Generate Graph Image
        graph_img_stream = graph_handler.visualize_graph(component_graph)

        graph_image_path = os.path.join(app.static_folder, "generated_graph.png")

        # Save the image for frontend display
        with open(graph_image_path, "wb") as f:
            f.write(graph_img_stream.getvalue())

        return jsonify({
            "message": "Component Graph generated successfully",
            "visualization": "/static/generated_graph.png"
        })

    except Exception as e:
        logging.error(f"Error processing code: {str(e)}")
        return jsonify({"error": f"Error generating component graph: {str(e)}"})


@app.route('/generate_repo_summary', methods=['POST'])
def generate_repo_summary():
    """API to generate structured repo summary and block diagram."""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        data = request.get_json()
        repo_owner = data.get("repo_owner")
        repo_name = data.get("repo_name")

        if not repo_owner or not repo_name:
            return jsonify({"error": "Repository details required"}), 400

        repo = CodeRepository(repo_owner, repo_name, repo_token)
        rag_handler = RAGHandler(embedding_generator)

        summary_data = rag_handler.generate_sequential_summary(repo)

        return jsonify(summary_data)

    except Exception as e:
        logging.error(f"Error generating repo summary: {str(e)}")
        return jsonify({"error": f"Error processing repo summary: {str(e)}"})

def allowed_file(filename):
    allowed_extensions = {'py', 'txt', 'md'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


if __name__ == "__main__":
    app.run(debug=True)
