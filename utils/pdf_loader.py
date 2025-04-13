from langchain.document_loaders import PyMuPDFLoader
import fitz  # PyMuPDF library for metadata extraction

def load_all_pdfs(file_paths):
    all_docs = []
    for path in file_paths:
        try:
            loader = PyMuPDFLoader(path)
            docs = loader.load()
            if docs:
                for doc in docs:  # Load all pages of each document
                    doc.metadata["source"] = path
                    all_docs.append(doc)
        except Exception as e:
            print(f"Error loading {path}: {str(e)}")
    return all_docs

def extract_metadata(file_path):
    metadata = {}
    try:
        pdf_document = fitz.open(file_path)
        metadata["title"] = pdf_document.metadata.get("title", "Unknown Title")
        metadata["author"] = pdf_document.metadata.get("author", "Unknown Author")
        metadata["creation_date"] = pdf_document.metadata.get("creationDate", "Unknown Date")
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {str(e)}")
    return metadata
