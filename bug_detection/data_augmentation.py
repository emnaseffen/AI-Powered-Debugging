import json

# Function to save the function string into a JSONL file
def save_json_l(function):
    # Normalize line endings to Unix-style (\n)
    normalized_function = function.replace('\r\n', '\n').replace('\r', '\n')
    
    # Save the function string in JSONL format
    with open('jsonl_format.jsonl', 'w', newline='\n') as jsonl_file:
        jsonl_file.write(json.dumps({"code": normalized_function}) + '\n')

# Function to read the JSONL file and save the code in an array
def read_json_l_to_array(filename):
    code_array = []
    with open(filename, 'r') as jsonl_file:
        for line in jsonl_file:
            json_obj = json.loads(line)
            code_array.append(json_obj["code"])  # Extract the code and append to the array
    return code_array

