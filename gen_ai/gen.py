import os
from google import genai 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")   
client = genai.Client(api_key=api_key)

def generate_answer (context,question):
    prompt = f"""Use the context below to answer the question. The context is from a PDF the user is reading

    If the context fully answers the question answer it 
    If the question asks about something connected to the context but not explicitly stated in it , you may use your own knowledge to make that connection
    If the context is completely unrelated to the question, say so and answer from general knowledge instead

    Context : {context}

    Question: {question}
    Answer:"""

    response = client.models.generate_content(
            model ="gemini-3.6-flash",
            contents = prompt
        )

    return response.text