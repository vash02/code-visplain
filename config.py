# config.py
import os

# Environment variable for security
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "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")  # You can set this as an environment variable
LLM_MODEL_NAME = "llama3.2"
EMBEDDING_MODEL_NAME = "microsoft/codebert-base"
