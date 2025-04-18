from langchain.llms import Ollama

def classify_document(text):
    llm = Ollama(model="mistral")
    prompt = (
        "Classify the type of document from the following text. "
        "Respond with categories like Resume, Research Paper, Invoice, Legal Document, etc.\n\n"
        f"{text[:1500]}\n\n"
        "Document Type:"
    )
    return llm(prompt)
