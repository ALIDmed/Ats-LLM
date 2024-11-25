from langchain_core.prompts import ChatPromptTemplate

system_prompt = """
You are an HR expert your task is to Analyze the following resume and determine its suitability for the job offer make sure to read careffuly the resume provided and see if the candidate is a good fit for the job offer. (see output options below):
Job Offer:
{job_offer}

Resume:
{resume}

Output: Provide a JSON object with 'category' as one of 'Forte Correspondance', 'Correspondance Moyenne', 'Mauvaise Correspondance', Make sure to classify and to keep in mind with the job offer.
This is an explanation for each category (with the criteria):
- Forte Correspondance: Ces candidats correspondent parfaitement aux exigences du poste et sont hautement qualifiés pour le rôle. and the condidate have almost all the skills required in the job offer.
- Correspondance Moyenne: Ces candidats sont partiellement adaptés au poste, mais nécessitent peut-être un examen plus approfondi ou un développement dans certains domaines.
- Mauvaise Correspondance: Ces candidats ne répondent pas aux exigences du poste, soit par manque d'expérience pertinente, de compétences ou d'autres facteurs. or if the candidate have no skills required in the job offer. or if the condidat has unrelated experience and skills to the job offer.


Make sure that the output is a JSON object with the key 'category' and the value as one of the categories above.
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt)
])