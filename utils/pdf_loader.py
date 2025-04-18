from langchain.document_loaders import PyMuPDFLoader
import fitz  
import pdfplumber
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
            logging.error(f"Error in [FUNCTION NAME or FILE]: {str(e)}", exc_info=True)
    return all_docs

def extract_metadata(file_path):
    metadata = {}
    try:
        pdf_document = fitz.open(file_path)
        metadata["title"] = pdf_document.metadata.get("title", "Unknown Title")
        metadata["author"] = pdf_document.metadata.get("author", "Unknown Author")
        metadata["creation_date"] = pdf_document.metadata.get("creationDate", "Unknown Date")
    except Exception as e:
        logging.error(f"Error in [FUNCTION NAME or FILE]: {str(e)}", exc_info=True)
    return metadata



def extract_tables(file_paths):
    tables = []
    for path in file_paths:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                if page.extract_tables():
                    tables.extend(page.extract_tables())
    return tables

def extract_charts(file_paths):
    charts = []
    for path in file_paths:
        doc = fitz.open(path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                charts.append(base_image["image"])
    return charts

def find_snippet_location(text_snippet, file_path):
    doc = fitz.open(file_path)
    for page_number, page in enumerate(doc):
        text_instances = page.search_for(text_snippet)
        if text_instances:
            return {
                "page": page_number,
                "bbox": text_instances[0],
                "file_path": file_path
            }
    return None


def render_highlighted_page(file_path, page_num, bbox):
    doc = fitz.open(file_path)
    page = doc[page_num]
    highlight = page.add_highlight_annot(bbox)
    pix = page.get_pixmap(dpi=150)
    return pix.tobytes("png")
