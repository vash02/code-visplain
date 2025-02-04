class CodeSummarizer:
    def __init__(self, llm_handler):
        self.llm_handler = llm_handler

    def summarize_code(self, file_name, file_content):
        """
        Summarizes the given code file.
        """
        prompt = f"Summarize the purpose and key components of the following code file:\n\nFile: {file_name}\n{file_content}"
        return self.llm_handler.query_llm(prompt)
