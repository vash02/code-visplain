from transformers import AutoTokenizer, AutoModel
import torch

import config


class EmbeddingGenerator:
    def __init__(self, model_name=config.EMBEDDING_MODEL_NAME):
        """
        Initialize the EmbeddingGenerator class with the pre-trained model and tokenizer.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def generate_embeddings(self, code_snippet):
        """
        Generate embeddings for a given code snippet using the pre-trained model.
        """
        # Tokenize the code snippet
        inputs = self.tokenizer(code_snippet, return_tensors="pt", truncation=True, padding=True, max_length=512)

        # Pass through the model to get the embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            # We are using the last hidden state and applying mean pooling
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()

        return embedding

    def generate_embeddings_batch(self, code_snippets):
        """
        Generate embeddings for a batch of code snippets.
        Returns a dictionary mapping file names to embeddings.
        """
        embeddings_dict = {}  # Store {filename: embedding}
        for file_name, _, snippet in code_snippets:
            embeddings_dict[file_name] = self.generate_embeddings(snippet)
        return embeddings_dict
