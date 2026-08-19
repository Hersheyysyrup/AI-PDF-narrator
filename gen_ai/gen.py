import os
from google import genai 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")   
client = genai.Client(api_key=api_key)

def generate_answer (context,question):
    prompt = f"""

    Context : {context}

    Question: {question}
    Answer:"""

    response = client.models.generate_content(
            model ="gemini-3.6-flash",
            contents = prompt
        )

    return response.text