from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import re 

def createModel():
    llm = ChatGroq(
            model='llama3-70b-8192',
            api_key='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',
            temperature=0,
            verbose=True,
        )
    return llm

def extract_code_block(text):
    #extract code block from generated code
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None
    
def generateBugFix(llm,java_code,bug):
    template = """
<|start_header_id|>system<|end_header_id|>
You are an honest and respectful code fixing assistant.
You are an expert in fixing code.
Please don't add any comments or any sample of usage.
This code {java_code} has a potential {bug} bug.
Your main objective is to fix the bug.
Please return all the code.
Please always return code between ```[code]```.
<|eot_id|>
"""
    prompt =PromptTemplate.from_template(template)
    prompt_text = prompt.format(java_code=java_code, bug=bug)
    changePrompt=prompt_text
    chain2 = llm | StrOutputParser()
    result = chain2.invoke(changePrompt)
    result =extract_code_block(result)
    return result




