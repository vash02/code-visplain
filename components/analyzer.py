import ast
import logging


class CodeAnalyzer:
    def __init__(self):
        pass
    def extract_functions_and_classes(self, code):
        """
        Extract functions, classes, and their relations from the provided Python code using AST.
        Returns:
            functions: list of tuples (function_name, function_code)
            classes: list of tuples (class_name, class_code)
            relations: list of tuples (caller_function, callee_function)
        """
        functions = []
        classes = []
        relations = []  # To store the relationships between functions

        try:
            # Ensure code is a valid string and not empty
            if isinstance(code, str):
                code = code.strip()  # Remove leading/trailing whitespace

                if not code:
                    raise ValueError("Code is empty after stripping whitespace.")

                # Parse the Python code into an AST (Abstract Syntax Tree)
                tree = ast.parse(code)
            else:
                raise ValueError("Code is not a valid string.")

            current_class = None  # Track the current class while traversing AST

            # Walk through the AST to find functions, classes, and relationships
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):  # Function node
                    function_code = ast.unparse(node)  # Get the actual function code

                    # Add function with or without class prefix
                    if current_class:
                        functions.append((f"{current_class}.{node.name}", function_code))
                    else:
                        functions.append((node.name, function_code))

                    # Check for function calls inside this function
                    for inner_node in ast.walk(node):
                        if isinstance(inner_node, ast.Call):  # Function call within the function
                            if isinstance(inner_node.func, ast.Name):  # Ensure it's a function call
                                called_function = inner_node.func.id
                                relations.append((node.name, called_function))

                elif isinstance(node, ast.ClassDef):  # Class node
                    class_code = ast.unparse(node)  # Get the actual class code
                    classes.append((node.name, class_code))
                    current_class = node.name  # Set the current class as we are inside this class
                else:
                    # Handle closing the current class scope
                    if isinstance(node, ast.FunctionDef):
                        current_class = None  # No longer in a class after the function is finished

        except SyntaxError as e:
            logging.error(f"SyntaxError while parsing code: {e}")
            return functions, classes, relations
        except ValueError as e:
            logging.error(f"ValueError: {e}")
            return functions, classes, relations
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return functions, classes, relations

        return functions, classes, relations


