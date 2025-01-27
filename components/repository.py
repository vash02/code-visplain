import requests

from components.analyzer import CodeAnalyzer


class CodeRepository:
    def __init__(self, repo_owner, repo_name, token):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token
        self.base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'

    def fetch_files_from_directory(self, dir_path=''):
        """
        Fetch the repository structure from GitHub, extract functions, classes, and method calls using AST.
        """
        url = self.base_url + dir_path
        response = requests.get(url, headers={'Authorization': f'token {self.token}'})

        function_files_list = []  # List to hold function chunks
        class_files_list = []  # List to hold class chunks
        metadata_files_list = []  # List to hold metadata files

        if response.status_code == 200:
            files = response.json()
            for file in files:
                if file['type'] == 'file':
                    file_url = file['download_url']
                    file_response = requests.get(file_url)
                    if file_response.status_code == 200:
                        file_content = file_response.text
                        file_name = file['name']

                        # Check if the file content is a string
                        if not isinstance(file_content, str):
                            print(f"Error: {file_name} content is not a string.")
                            continue  # Skip this file and move on to the next

                        # Process the file content only if it's a Python file
                        if file_name.endswith('.py'):
                            analyzer = CodeAnalyzer()
                            functions, classes, relations = analyzer.extract_functions_and_classes(file_content)
                            for func_name, func_code in functions:
                                function_files_list.append((file_name, func_name, func_code))
                            for class_name, class_code in classes:
                                class_files_list.append((file_name, class_name, class_code))
                        else:
                            metadata_files_list.append(file_name)
                    else:
                        print(f"Error fetching content from {file_name}, Status code: {file_response.status_code}")
                elif file['type'] == 'dir':
                    sub_function_files_list, sub_class_files_list, sub_metadata_files_list = self.fetch_files_from_directory(
                         file['path']
                    )
                    function_files_list.extend(sub_function_files_list)
                    class_files_list.extend(sub_class_files_list)
                    metadata_files_list.extend(sub_metadata_files_list)
        else:
            print(f'Error: {response.status_code}, {response.text}')

        return function_files_list, class_files_list, metadata_files_list

    # def fetch_file_content(self, file_url):
    #     """
    #     Fetch content of a single file using its download URL.
    #     """
    #     file_response = requests.get(file_url)
    #     if file_response.status_code == 200:
    #         return file_response.text
    #     else:
    #         print(f"Error fetching content from {file_url}")
    #         return ''