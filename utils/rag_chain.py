from langchain.llms import Ollama
from langchain.chains import RetrievalQA

def get_qa_chain(db):
    llm = Ollama(model="mistral")
    retriever = db.as_retriever()
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
