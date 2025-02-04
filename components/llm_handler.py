import ollama
import config
class LLMHandler:
    def __init__(self, model_name="llama3.2"):
        self.model_name = config.LLM_MODEL_NAME

    def query_llm(self, prompt):
        """
        Queries LLaMA model with a given prompt.
        """
        try:
            response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
            return response["message"]["content"]
        except Exception as e:
            return f"Error querying LLaMA: {str(e)}"
