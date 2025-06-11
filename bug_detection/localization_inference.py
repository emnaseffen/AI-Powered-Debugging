import numpy as np
from difflib import SequenceMatcher
from transformers import RobertaTokenizerFast, RobertaForTokenClassification
import streamlit as st

# Load the model and tokenizer

def generate_char_mask(original_src, changed_src):
    s = SequenceMatcher(None, original_src, changed_src)
    opcodes = [x for x in s.get_opcodes() if x[0] != "equal"]
    
    original_labels = np.zeros_like(list(original_src), dtype=np.int32)
    for _, i1, i2, _, _ in opcodes:
        original_labels[i1: max(i1+1, i2)] = 1

    return original_labels.tolist()

def predict(tokenizer, model, error, source,model_path):
    model = RobertaForTokenClassification.from_pretrained(model_path)
    tokenizer = RobertaTokenizerFast.from_pretrained("microsoft/codebert-base")
    if not isinstance(source, list):
        source = [source]
        error = [error]
    
    tokenized_inputs = tokenizer(text=error, text_pair=source, padding=True, truncation=True, return_tensors="pt").to(model.device)
    tokenized_labels = np.argmax(model(**tokenized_inputs)['logits'].cpu().detach().numpy(), 2)
    
    all_labels = []
    for i in range(tokenized_labels.shape[0]):
        labels = [0] * len(source[i])
        for j, label in enumerate(tokenized_labels[i]):
            if tokenized_inputs.token_to_sequence(i, j) != 1:
                continue

            word_id = tokenized_inputs.token_to_word(i, j)
            cs = tokenized_inputs.word_to_chars(i, word_id, sequence_index=1)
            if cs.start == cs.end:
                continue
            labels[cs.start:cs.end] |= tokenized_labels[i, j]
        
        all_labels.append(labels)
    
    return all_labels

def color_source(source_code, mask):
    colored_code = ""
    for i, char in enumerate(source_code):
        if mask[i] == 1:
            # Highlight the buggy part in red
            colored_code += f"<span style='color:red;'>{char}</span>"
        else:
            colored_code += char
    # Replace newlines with <br> to ensure correct display in HTML
    colored_code = colored_code.replace("\n", "<br>")
    return colored_code

def display_example(source_code,mask):
    st.write("##### The localization of the bug")
    # Apply the color to the buggy code and render as HTML with line breaks
    colored_code = f"<div style='font-family:monospace;'>{color_source(source_code, mask)}</div>"
    st.markdown(colored_code, unsafe_allow_html=True)  # Use unsafe_allow_html for rendering HTML

