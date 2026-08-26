import pytesseract
from pdf2image import convert_from_path
from langchain_core.documents import Document

def pdf_load_ocr(pdf_path):
    """
    Convert PDF pages to image and exteract text using Tesseract OCR.
    Return a list of LangChain Document objects.
    """

    #pdf to image conversion
    pages = convert_from_path (
        pdf_path, 
        dpi=300,
        poppler_path= r"C:\Users\Harshit\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin" )

    documents = []

    for page_number, page_image in enumerate(pages, start =1 ):

        #image page extract
        text = pytesseract.image_to_string(page_image)

        if text.strip():
            documents.append(
                Document(
                     page_content = text,
                    metadata = {
                        "source": pdf_path,
                        "page": page_number

                }
            )
        ) 
    print(f"OCr extracted text from {len(documents)}pages")

    return documents 


#temperory working 
if __name__ == "__main__":
    pdf_path = r"C:\Users\Harshit\OneDrive\Attachments\Desktop\RAG.pdf"

    documents = pdf_load_ocr(pdf_path)

    print("Number of documents:", len(documents))
    print("First page text:")
    print(documents[0].page_content[:1000])