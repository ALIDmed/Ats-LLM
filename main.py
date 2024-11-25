from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from utils import read_pdf
from prompt import prompt_template
from concurrent.futures import ThreadPoolExecutor
import concurrent
import os
import shutil
import json
from tqdm import tqdm
load_dotenv()

RESUME_DIR = './CV'

with open("./job_offer.txt", "r", encoding='utf-8') as file:
    job_offer = file.read()

results = []
categories = {
    "Forte Correspondance": "Forte Correspondance",
    "Correspondance Moyenne": "Correspondance Moyenne",
    "Mauvaise Correspondance": "Mauvaise Correspondance",
}

llm = ChatGroq(groq_api_key=os.getenv('GROQ_API_KEY'), model_name="llama-3.1-8b-instant")
chain = prompt_template | llm | JsonOutputParser()

for category in categories.values():
    os.makedirs(category, exist_ok=True)

def process_resume(filename):
    resume_content = read_pdf(os.path.join(RESUME_DIR, filename))
    res = chain.invoke({"resume": resume_content, "job_offer":job_offer})
    if isinstance(res, dict):
        category = res.get('category', 'Mauvaise Correspondance')
    else:
        category = 'Mauvaise Correspondance'

    shutil.copy(
        os.path.join(RESUME_DIR, filename),
        os.path.join(categories[category], filename)
    )
    
    return {"candidate": filename, "status": category}

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(process_resume, filename): filename for filename in os.listdir(RESUME_DIR) if filename.endswith('.pdf')}
    for future in tqdm(concurrent.futures.as_completed(futures)):
        try:
            result = future.result()
            results.append(result)
        except Exception as e:
            print(f"Error processing {futures[future]}: {e}")

# for filename in tqdm(os.listdir(RESUME_DIR)):
#     resume_content = read_pdf(os.path.join(RESUME_DIR, filename))
#     res = chain.invoke({"resume": resume_content, "job_offer":job_offer})
    
#     if isinstance(res, dict):
#         category = res.get('category', 'irrelevant')
#     else:
#         print('continue')
#         category = 'Mauvaise Correspondance'
    
#     shutil.copy(
#         os.path.join(RESUME_DIR, filename), 
#         os.path.join(categories[category], filename)
#     )
#     results.append({"candidate": filename, "status": category, "why": res.get('why', 'ma3rftch')})

# print(results)