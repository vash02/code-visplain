# config.py
import os

# Environment variable for security
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "<YOUR_GIT_TOKEN>")  # You can set this as an environment variable
LLM_MODEL_NAME = "llama3.2"
EMBEDDING_MODEL_NAME = "microsoft/codebert-base"
