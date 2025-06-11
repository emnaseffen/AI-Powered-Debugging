import streamlit as st
import zipfile
import io
from transformers import T5ForConditionalGeneration, RobertaTokenizer
from detection_inference import *
from data_augmentation import *
from ast_python import *
from localization_inference import *
from extract_java_functions import *
from bug_fix import *
import hashlib

# Set the title of the Streamlit app
st.title("Bug Detection, Localization and Fixing")

# Create a file uploader that accepts only ZIP files
uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")

def extract_java_files(file_list):
    return [f for f in file_list if f.endswith('.java')]

def generate_key_from_content(content):
    return hashlib.md5(content.encode()).hexdigest()

# Check if a file was uploaded
if uploaded_file is not None:
    if uploaded_file.name.endswith(".zip"):
        # Read the uploaded ZIP file
        with zipfile.ZipFile(io.BytesIO(uploaded_file.read()), 'r') as zip_ref:
            # Display the list of files in the ZIP archive
            st.write("Files in the ZIP archive:")
            file_list = zip_ref.namelist()
            st.write(file_list)

            # Extract Java files
            java_files = extract_java_files(file_list)

            if java_files:
                st.write("##### Java files:")
                for file_name in java_files:
                    with zip_ref.open(file_name) as file:
                        content = file.read().decode('utf-8')
                        st.write(f"##### Content of {file_name}:")
                        functions = extract_functions_from_java_class(content)
                        # Display extracted functions
                        for index,(func_name, combined_content) in enumerate(functions.items()):
                            save_json_l(combined_content)
                            code_array = read_json_l_to_array('jsonl_format.jsonl')
                            if code_array:
                                model_path = 'C:/Users/Seffen Emna/Documents/Novobit_debugging/bug_detection/models/java_detection_model'
                                model = T5ForConditionalGeneration.from_pretrained(model_path)
                                st.code(combined_content,language='java')
                                tokenizer = RobertaTokenizer.from_pretrained(model_path)
                                prediction = predict_detection(tokenizer, model, code_array)[0]
                                st.code(f"{prediction}")
                                model_path = 'C:/Users/Seffen Emna/Documents/Novobit_debugging/bug_detection/models/java_local_model'
                                mask = predict(tokenizer, model, prediction,combined_content,model_path)[0]
                                if prediction != "Accepted":
                                    display_example(combined_content, mask)
                                    st.markdown("")
                                    st.write("##### The bug")
                                    st.code(f"{prediction}")
                                    func_body_hash = generate_key_from_content(combined_content)
                                    button_key = f'suggest_fix_button_{index}_{func_body_hash}'
                                    if st.button('Suggest Fix', type="primary", key=button_key):
                                       llm = createModel()
                                       result = generateBugFix(llm, combined_content, prediction)
                                       st.write("##### Suggested Fix")
                                       st.code(result)
                            else:
                                st.write(f"##### No valid code found in function **{func_name}**.")


            # If you also want to process Python files, keep the following code
            python_files = [f for f in file_list if f.endswith('.py')]

            if python_files:
                # Extract and process each Python file
                for file_name in python_files:
                    with zip_ref.open(file_name) as file:
                        content = file.read().decode('utf-8')  # Decode to convert bytes to string
                        st.write(f"##### Content of {file_name}:")
                        # Extract functions from the content
                        functions = extract_functions_from_content(content)

                        # Process each function
                        for index,(func_name, func_body)in enumerate(functions.items()):
                            save_json_l(func_body)
                            code_array = read_json_l_to_array('jsonl_format.jsonl')
                            
                            # Check if the code array is not empty
                            if code_array:
                                st.code(code_array[0], language='python')
                                model_path = 'C:/Users/Seffen Emna/Documents/Novobit_debugging/bug_detection/models/python_var_model'
                                model = T5ForConditionalGeneration.from_pretrained(model_path)
                                tokenizer = RobertaTokenizer.from_pretrained(model_path)
                                prediction = predict_detection(tokenizer, model, code_array)[0]
                                st.code(f"{prediction}")
                                model_path = 'C:/Users/Seffen Emna/Documents/Novobit_debugging/bug_detection/models/python_localization_model'
                                mask = predict(tokenizer, model, prediction, func_body,model_path)[0]
                                # Streamlit app logic
                                if prediction != "Accepted":
                                    display_example(func_body, mask)
                                    st.markdown("")
                                    st.write("##### The bug")
                                    st.code(f"{prediction}")
                                    func_body_hash = generate_key_from_content(func_body)
                                    button_key = f'suggest_fix_button_{index}_{func_body_hash}'
                                    if st.button('Suggest Fix', type="primary", key=button_key):
                                       llm = createModel()
                                       result = generateBugFix(llm, func_body, prediction)
                                       st.write("##### Suggested Fix")
                                       st.code(result)
                            else:
                                st.write(f"##### No valid code found in function **{func_name}**.")
    else:
        st.error("The uploaded file is not a ZIP file.")
