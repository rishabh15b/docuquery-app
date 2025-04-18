import fitz  # PyMuPDF
import io
from PIL import Image

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
    page.add_highlight_annot(bbox)
    pix = page.get_pixmap(dpi=150)
    return pix.tobytes("png")