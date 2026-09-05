import streamlit as st
import os
from gen_ai.gen import generate_answer
from coqui.tts import speak
from document_loaders.ocr import pdf_load_ocr
from text_splitters.splitters import split_documents
from embeddings.embeddings import get_embedding_model
from vector_store.chroma import create_vector_store
from retriever.retriever import get_mmr_retriever

st.set_page_config(page_title="PDF to Audio Generator", layout="wide")

if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: upload + settings ---
with st.sidebar:
    st.header("PDF to Audio Generator")
    uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

    if uploaded_file and st.button("Load PDF", use_container_width=True):
        with st.spinner("Reading and indexing..."):
            temp_path = os.path.join("temp_uploads", uploaded_file.name)
            os.makedirs("temp_uploads", exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            documents = pdf_load_ocr(temp_path)
            chunks = split_documents(documents)
            embedding_model = get_embedding_model()
            vector_store = create_vector_store(chunks, embedding_model)

            st.session_state.retriever = get_mmr_retriever(vector_store)
            st.session_state.messages = []

        st.success(f"Indexed {len(chunks)} chunks")

    st.divider()
    st.caption("Ask Questions:")

# --- Main: chat thread ---
st.title("Good to see you!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("audio") and os.path.exists(msg["audio"]):
            st.audio(msg["audio"])
        if msg.get("pages"):
            st.caption("Sources: " + ", ".join(f"Page {p}" for p in msg["pages"]))

if question := st.chat_input("Ask a question: "):
    if st.session_state.retriever is None:
        st.warning("Upload and load a PDF first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                docs = st.session_state.retriever.invoke(question)
                context = "\n".join(doc.page_content for doc in docs)
                answer = generate_answer(context, question)
                audio_path = speak(answer)
                pages = sorted(set(doc.metadata.get("page") for doc in docs if doc.metadata.get("page")))

            st.write(answer)
            if audio_path and os.path.exists(audio_path):
                st.audio(audio_path)
            if pages:
                st.caption("Sources: " + ", ".join(f"Page {p}" for p in pages))

        st.session_state.messages.append({
            "role": "assistant", "content": answer, "audio": audio_path, "pages": pages
        })