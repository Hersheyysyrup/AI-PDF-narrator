from document_loaders.pdf import load_pdf
from text_splitters.splitters import split_documents
from embeddings.embeddings import get_embedding_model

pdf_path = "data/rag.pdf"

documents = load_pdf(pdf_path)
print(f"Loaded {len(documents)} pages")

chunks = split_documents(documents)
print(f"Created {len(chunks)}chunks")

embedding_model = get_embedding_model()
print("Embedding Model Loaded")