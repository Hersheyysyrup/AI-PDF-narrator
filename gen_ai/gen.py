import os
from google import genai 
from dotenv import load_dotenv
from google.genai import errors as genai_errors
from openai import OpenAI

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")   
gemini_client = genai.Client(api_key=gemini_api_key)

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key = openai_api_key)

def build_prompt (context,question):
    return f"""Use the context below to answer the question. The context is from a PDF the user is reading

    If the context fully answers the question answer it 
    If the question asks about something connected to the context but not explicitly stated in it , you may use your own knowledge to make that connection
    If the context is completely unrelated to the question, say so and answer from general knowledge instead

    Context : {context}

    Question: {question}
    Answer:"""

def generate_answer(context, question):

    prompt = build_prompt(context, question)

    try:

        # Primary: Gemini
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as exp:

        print(f"[Gemini failed: {exp}] Falling back to OpenAI...")

        # Fallback: OpenAI
        response = openai_client.responses.create(
            model="gpt-5-mini",
            messages = [{"role": "user", "content": prompt}]
        )

        return response.output_text
