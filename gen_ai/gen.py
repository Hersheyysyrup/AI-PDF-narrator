from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def generate_answer(context, question):

    prompt = f"""
You are an AI assistant that answers questions based only on the provided PDF context.

Context:
{context}

Question:
{question}

Answer using only the information from the context.
If the answer is not present in the context, say that you could not find the answer in the PDF.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text