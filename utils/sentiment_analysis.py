import fitz  # PyMuPDF
from textblob import TextBlob

def analyze_sentiment_by_page(file_paths):
    all_results = []

    for path in file_paths:
        doc = fitz.open(path)
        results = []

        for i, page in enumerate(doc):
            text = page.get_text()
            blob = TextBlob(text)
            results.append({
                "page": i + 1,
                "polarity": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity
            })

        all_results.append({
            "file": path,
            "pages": results
        })

    return all_results