import gradio as gr
from gen_ai.gen import generate_answer
from coqui.tts import speak
from document_loaders.ocr import pdf_load_ocr
from embeddings.embeddings import get_embedding_model
from text_splitters.splitters import split_documents
from vector_store.chroma import create_vector_store
from retriever.retriever import get_mmr_retriever

current_retriever = {"retriever":None}

def handle_upload(pdf_file):
    if pdf_file is None:
        return "Please upload a file"

    documents = pdf_load_ocr(pdf_file.name)
    embedding_model = get_embedding_model()
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks, embedding_model)

    current_retriever["retriever"] = get_mmr_retriever(vector_store)

    return f"PDF loaded succesfully! Please ask your question"

def handle_question(question):
    retriever = current_retriever["retriever"]
    docs = retriever.get_relevant_documents(question)
    context = "\n".join(doc.page_content for doc in docs)
    answer = generate_answer(question, context)

    audio_path = speak(answer)

    return answer, audio_path

with gr.Blocks(title = "TEXT TO AUDIO GENERATOR") as demo:
    gr.Markdown("# TEXT TO AUDIO GENERATOR")
    gr.Markdown("Uplaod a PDF to generate an audio file")

    with gr.Row():
        pdf_input = gr.File(label="Upload your PDF", file_types=[".pdf"])
        upload_status = gr.Textbox(label ="Status", interactive = False)

    upload_btn = gr.Button("Upload PDF")
    upload_btn.click(fn = handle_upload, inputs = pdf_input, outputs = upload_status)

    gr.Markdown("----")

    question_input = gr.Textbox(label = "Ask a question")
    ask_btn = gr.Button("Ask")

    answer_output = gr.Textbox(label = "Answer", interactive = False)
    audio_output = gr.Audio(label = "Audio", type = "filepath")

    ask_btn.click(fn = handle_question, inputs = question_input, outputs = [answer_output, audio_output])

if __name__ == "__main__":
    demo.launch()