from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
import os

def create_store(docs, persist_dir="my_faiss_index"):
    embeddings = OllamaEmbeddings(model="mistral")
    if os.path.exists(persist_dir):
        db = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)
        db.add_documents(docs)
    else:
        db = FAISS.from_documents(docs, embeddings)
    db.save_local(persist_dir)
    return db

def load_store(persist_dir="my_faiss_index"):
    embeddings = OllamaEmbeddings(model="mistral")
    faiss_file = os.path.join(persist_dir, "index.faiss")
    pkl_file = os.path.join(persist_dir, "index.pkl")
    
    if os.path.exists(faiss_file) and os.path.exists(pkl_file):
        return FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)
    else:
        raise FileNotFoundError("FAISS index files not found. Please upload PDFs and create index first.")
