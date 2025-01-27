import io

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS  # For CORS
import os
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('Agg')  # Use Agg backend for non-GUI rendering
import logging
from components.repository import CodeRepository
from components.analyzer import CodeAnalyzer
from components.graph_handler import GraphHandler
from components.embedding_generator import EmbeddingGenerator
import config

app = Flask(__name__, static_folder='frontend/build', static_url_path='/static')

# Enable CORS for all domains
CORS(app)

# Setup logging to capture any issues
logging.basicConfig(level=logging.DEBUG)

# Initialize components with config
embedding_generator = EmbeddingGenerator()
code_analyzer = CodeAnalyzer()

# Initialize CodeRepository with GitHub token from config
repo_token = config.GITHUB_TOKEN


@app.route('/')
def index():
    return send_from_directory('frontend/build', 'index.html')


@app.route('/upload', methods=['POST'])
def upload_code():
    # Log the form data to check if it's coming through correctly
    upload_option = request.form.get('uploadOption')  # Get selected option (file or repo)
    logging.debug(f"Upload option selected: {upload_option}")

    if upload_option == 'file':
        # Case 1: File upload
        if 'code_file' not in request.files:
            logging.error("No file part")
            return jsonify({"error": "No file part"})

        file = request.files['code_file']

        if file.filename == '':
            logging.error("No selected file")
            return jsonify({"error": "No selected file"})

        if file and allowed_file(file.filename):
            # Save the file
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            # Step 1: Read file content
            with open(file_path, 'r') as f:
                file_content = f.read()

            # Step 2: Process the code
            return process_code(file_content)

    elif upload_option == 'repo':
        # Case 2: Repo details input
        repo_owner = request.form['repo_owner']
        repo_name = request.form['repo_name']

        logging.debug(f"Received repo details: {repo_owner}, {repo_name}")

        # Step 1: Fetch code from the repository using the provided details
        repo = CodeRepository(repo_owner, repo_name, repo_token)

        # Step 2: Process the code
        return process_code(repo)

    else:
        logging.error(f"Invalid input option: {upload_option}")
        return jsonify({"error": "Invalid input option selected"})


def process_code(repo):
    try:
        # Generate embeddings for the code
        functions, classes, relations = repo.fetch_files_from_directory()

        # Create the component graph based on extracted code
        graph_handler = GraphHandler(functions, classes)
        component_graph = graph_handler.create_component_graph()

        # Generate the graph image as a stream
        graph_img_stream = graph_handler.visualize_graph(component_graph)

        # Save the image to the static folder for serving
        image_path = os.path.join(app.static_folder, "generated_graph.png")
        with open(image_path, "wb") as f:
            f.write(graph_img_stream.getvalue())

        return jsonify({
            "message": "Graph generated successfully",
            "visualization": "/static/generated_graph.png"
        })
    except Exception as e:
        return jsonify({"error": f"Error generating graph image: {str(e)}"})

@app.route('/generate_graph')
def generate_graph():
    try:
        # Generate the graph image stream
        graph_img_stream = generate_graph_image()

        # Send the image to the frontend
        return send_file(graph_img_stream, mimetype='image/png', as_attachment=False, download_name='graph.png')

    except Exception as e:
        return jsonify({"error": f"Error generating graph: {str(e)}"})


def generate_graph_image():
    # Example plot to verify
    plt.figure(figsize=(12, 12))
    plt.plot([1, 2, 3], [1, 4, 9], label="Sample Plot")
    plt.title("Sample Graph")
    plt.grid(True)
    plt.legend()

    # Save the plot to a BytesIO stream
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)  # Rewind the stream to the start

    return img_stream

def allowed_file(filename):
    allowed_extensions = {'py', 'txt', 'md'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


if __name__ == "__main__":
    app.run(debug=True)
