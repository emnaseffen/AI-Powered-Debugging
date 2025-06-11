import ast

def extract_functions_from_content(file_content):
    try:
        # Parse the content into an AST
        tree = ast.parse(file_content)
    except SyntaxError:
        # If there's a syntax error, return the original content
        return {'__all_code__': file_content}

    # Extract function names and their bodies
    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            function_body = ast.get_source_segment(file_content, node)
            functions[function_name] = function_body

    # If no functions were found, return the original content
    if not functions:
        return {'__all_code__': file_content}

    return functions
