from document_loaders.pdf import load_pdf
from text_splitters.splitters import split_documents
from embeddings.embeddings import get_embedding_model
from vector_store.chroma import create_vector_store
from retriever.retriever import get_mmr_retriever
from gen_ai.gen import generate_answer

pdf_path = "AI PDF narrator/data/rag.pdf"

documents = load_pdf(pdf_path)
print(f"Loaded {len(documents)} pages")

chunks = split_documents(documents)
print(f"Created {len(chunks)}chunks")

embedding_model = get_embedding_model()
print("Embedding Model Loaded")

vector_store = create_vector_store(chunks, embedding_model)
print("Vector store created")

def ask(question,retriever):
    docs = retriever.invoke(question)
    context = "\n\n".join(
        doc.page_content for doc in docs
        )
    answer = generate_answer(context,question)
    return answer

def main():
    retriever = get_mmr_retriever(vector_store)

    print("Ask questions about your PDF. Type'exit' to quit.\n")
    while True:
        question = input("Ask a Question: ")
        if question.lower() in ("exit","quit", "q"):
            print("Goodbye!")
            break

        answer = ask(question, retriever)
        print(f"\nAnswer : {answer}\n")

if __name__ == "__main__":
    main()
