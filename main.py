from document_loaders.pdf import load_pdf
from text_splitters.splitters import split_documents
from embeddings.embeddings import get_embedding_model
from vector_store.chroma import create_vector_store

pdf_path = "AI PDF narrator/data/rag.pdf"

documents = load_pdf(pdf_path)
print(f"Loaded {len(documents)} pages")

chunks = split_documents(documents)
print(f"Created {len(chunks)}chunks")

embedding_model = get_embedding_model()
print("Embedding Model Loaded")

vector_store = create_vector_store(chunks, embedding_model)
print("Vector store created")