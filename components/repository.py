import requests
from components.analyzer import CodeAnalyzer

class CodeRepository:
    def __init__(self, repo_owner, repo_name, token):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token
        self.base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'
        self.analyzer = CodeAnalyzer()  # Initialize AST Analyzer

        # **Cache for fast lookups**
        self.file_cache = {}  # {file_name: raw_content}
        self.function_cache = {}  # {file_name: [(func_name, func_code)]}
        self.class_cache = {}  # {file_name: [(class_name, class_code)]}
        self.metadata_files = []  # List of metadata files

    def fetch_files_from_directory(self, dir_path=''):
        """
        Fetch repository structure, extract functions, classes, and method calls using AST.
        Returns:
            functions: list of (file_name, func_name, func_code)
            classes: list of (file_name, class_name, class_code)
            metadata_files: list of file names (non-Python)
        """
        url = self.base_url + dir_path
        response = requests.get(url, headers={'Authorization': f'token {self.token}'})

        function_files_list = []
        class_files_list = []
        metadata_files_list = []

        if response.status_code == 200:
            files = response.json()
            for file in files:
                file_name = file['name']

                if file['type'] == 'file':
                    file_content = self._fetch_and_cache_file(file_name, file['download_url'])

                    if file_name.endswith('.py'):
                        if file_name not in self.function_cache or file_name not in self.class_cache:
                            functions, classes, relations = self.analyzer.extract_functions_and_classes(file_content)
                            self.function_cache[file_name] = functions
                            self.class_cache[file_name] = classes

                        function_files_list.extend([(file_name, *func) for func in self.function_cache[file_name]])
                        class_files_list.extend([(file_name, *cls) for cls in self.class_cache[file_name]])
                    else:
                        metadata_files_list.append(file_name)

                elif file['type'] == 'dir':
                    sub_function_files_list, sub_class_files_list, sub_metadata_files_list = self.fetch_files_from_directory(
                        file['path']
                    )
                    function_files_list.extend(sub_function_files_list)
                    class_files_list.extend(sub_class_files_list)
                    metadata_files_list.extend(sub_metadata_files_list)

        else:
            print(f'Error fetching repository contents: {response.status_code}, {response.text}')

        return function_files_list, class_files_list, metadata_files_list

    def _fetch_and_cache_file(self, file_name, file_url):
        """
        Fetches the raw file content **once** and stores it in a cache.
        """
        if file_name in self.file_cache:
            return self.file_cache[file_name]  # **Fast lookup**

        response = requests.get(file_url)
        if response.status_code == 200:
            self.file_cache[file_name] = response.text  # Cache the file content
            return response.text
        else:
            print(f"Error fetching content for {file_name}, Status code: {response.status_code}")
            return None

    def get_file_content(self, file_name):
        """
        Retrieves file content instantly using the cached dictionary.
        """
        return self.file_cache.get(file_name, None)  # **Fast lookup instead of iteration**
