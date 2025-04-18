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

```
├── app.py                # Main application file
├── utils/                # Utility scripts for core functionalities
│   ├── pdf_loader.py     # Functions for loading and parsing PDFs
│   ├── chunking.py       # Logic for splitting documents into chunks
│   ├── vector_store.py   # Functions for creating and managing the vector store
│   ├── prompt_router.py  # Handles dynamic prompt generation based on query type
│   ├── qa_chain.py       # Sets up the question-answering chain
├── uploaded_pdfs/        # Directory for storing uploaded PDF files
├── my_faiss_index/       # Directory for storing the FAISS vector index
└── README.md             # Project documentation
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.9+
- [Ollama installed](https://ollama.com)
- `streamlit` and other Python dependencies

### Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/rishabh15b/docuquery.git
cd docuquery

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull the model
ollama pull mistral-small3.1

# 5. Run the app
streamlit run app.py

# 6. Ensure Ollama server is running
ollama serve

7. Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧠 Usage

1. **Upload** one or more PDF files using the sidebar.
2. **Adjust** chunk size and overlap as needed.
3. **Enable desired features:**
   - 📊 **Table Extraction**
   - 📈 **Chart Extraction**
   - 🧠 **Sentiment Analysis**
   - 🖍️ **Visual Source Highlighting**
4. **Ask questions** like:
   - "Who is the author?"
   - "Summarize this document"
   - "List the key points on page 3"
5. **View** the LLM-generated answer with source highlights.
6. **Download** sentiment analysis as a CSV file (if applicable).

---

## 🌟 Current Model: Mistral Small 3.1

DocuQuery currently uses the **Mistral Small 3.1** model from Ollama, offering:

- 🧠 **Enhanced Reasoning** – Ideal for complex queries and summarization.
- 🪶 **Lightweight Deployment** – Runs efficiently on devices like Macs, Linux, or Windows machines.
- 📏 **Long Context Window** – Supports up to **128k tokens** for deep document understanding.
- ⚡ **Fast Performance** – Provides responsive answers with low latency.

🔗 [Learn more about Mistral Small 3.1](https://ollama.com/library/mistral-small3.1)

---

## 🔮 Upcoming Enhancements

- 🧠 **Named Entity Recognition (NER)** using spaCy
- 🧾 **Document Classification** (Resume, Legal, Invoice, etc.)
- 📘 **Section-Based Navigation & Summarization**
- 🌐 **Multilingual Query Support**
- 🔧 **Model Selector** (switch between Mistral, GPT-4, Claude, etc.)
- 📊 **Dashboard View** with tabs for:
  - Sentiment Trends
  - Extracted Tables
  - Q&A History

---

## 🤝 Contribution Guidelines

We welcome contributions! To contribute:

# Fork the repository
git checkout -b feature/my-feature

# Make your changes
git commit -m "Add feature: my-feature"

# Push and open a pull request
git push origin feature/my-feature

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

