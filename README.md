# 📄 DocuQuery

**DocuQuery** is a powerful **Retrieval-Augmented Generation (RAG)** application built using **LangChain**, **Streamlit**, and **Ollama**, enabling users to interact with their uploaded PDFs through natural language queries. With advanced AI capabilities, DocuQuery provides accurate answers, summaries, and insights based on document content.

![image](https://github.com/user-attachments/assets/1bac008a-70f7-468e-a8ba-e35fd43ca1f0)

---

## 🚀 Features

- **PDF Uploads:** Upload one or multiple PDF files for analysis.
- **Document Chunking:** Automatically split large documents into manageable chunks for efficient processing.
- **Vector Store Integration:** Store document embeddings using FAISS for fast and accurate retrieval.
- **Question Answering:** Ask questions about your documents and receive detailed answers powered by Ollama's Mistral model.
- **Dynamic Prompting:** Automatically adjust prompts based on query type (e.g., summarization, keyword extraction).
- **Query History:** View, export, or clear past queries and answers.
- **Source Transparency:** Display snippets of source documents used to generate answers.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**: Interactive web interface.
- **LangChain**: Framework for building RAG pipelines.
- **Ollama**: Local language model integration (currently using the Mistral model).
- **FAISS**: Vector store for efficient document retrieval.

---

## 📂 Project Structure

├── app.py # Main application file
├── utils/
│ ├── pdf_loader.py # Functions for loading PDFs
│ ├── chunking.py # Document chunking logic
│ ├── vector_store.py # Vector store creation and loading
│ ├── prompt_router.py # Dynamic prompt generation
│ ├── qa_chain.py # QA chain setup
├── uploaded_pdfs/ # Directory for uploaded PDFs
├── my_faiss_index/ # Directory for vector store
└── README.md # Project documentation

---

## ⚙️ Installation

### Prerequisites
1. Python 3.9 or higher.
2. Ollama installed locally. [Install Ollama](https://ollama.com).
3. Streamlit library installed.

### Steps to Set Up the Project

1. Clone the repository:
git clone https://github.com/rishabh15b/docuquery.git
cd docuquery

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Pull the Mistral model:
ollama pull mistral-small3.1 # Lightweight version with enhanced reasoning and long context support.

5. Start the Streamlit app:
streamlit run app.py

6. Ensure Ollama server is running:
ollama serve

7. Open the app in your browser at `http://localhost:8501`.

---

## 🧠 Usage

1. Upload one or more PDF files through the sidebar.
2. Adjust chunking settings (chunk size and overlap) as needed.
3. Type your question in the input box (e.g., "Summarize this document").
4. View the answer along with source document snippets.
5. Access query history in the sidebar to review past interactions.

---

## 🌟 Current Model: Mistral Small 3.1

This project currently uses the **Mistral Small 3.1** model from Ollama, which offers:

- **Lightweight Deployment:** Runs efficiently on devices like a Mac with 32GB RAM or an RTX 4090 GPU.
- **Enhanced Reasoning:** State-of-the-art reasoning capabilities, perfect for answering complex queries based on document content.
- **Long Context Window:** Supports up to 128k tokens, making it ideal for analyzing large documents.
- **Fast Response Times:** Provides quick conversational assistance with low latency.

For more details about Mistral Small 3.1, visit [Ollama Mistral Small 3.1](https://ollama.com/library/mistral-small3.1).

---

## 🌟 Key Features to Add Next

- **Multilingual Support:** Enable queries in multiple languages.
- **Customizable Prompts:** Let users define query styles dynamically.
- **Cloud Integration:** Allow users to upload files from Google Drive or Dropbox.
- **Analytics Dashboard:** Display statistics about user activity and document usage.

---

## 🤝 Contribution Guidelines

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch:
git checkout -b feature/<feature_name>
3. Commit your changes:
git commit -m "Add <feature_name>"
4. Push to your branch:
git push origin feature/<feature_name>
5. Create a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed by [Rishabh Balaiwar](https://github.com/rishabh15b). Feel free to reach out for questions or collaboration opportunities!

---

## 📞 Contact

For support or inquiries, contact me at:
- Email: <rbalaiwar@gmail.com>
- GitHub: [Your GitHub Profile](https://github.com/rishabh15b)

