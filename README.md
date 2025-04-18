# 📄 DocuQuery

**DocuQuery** is a powerful **Retrieval-Augmented Generation (RAG)** application built using **LangChain**, **Streamlit**, and **Ollama**, enabling users to interact with their uploaded PDFs through natural language queries. With advanced AI capabilities, DocuQuery provides accurate answers, summaries, insights, visual highlights, table/chart extraction, and page-wise sentiment analysis.

---

## 🚀 Features Implemented

- 📁 **PDF Uploads** — Upload one or multiple PDF files for analysis.
- ✂️ **Document Chunking** — Automatically split large documents into configurable chunks for efficient processing.
- 📦 **Vector Store (FAISS)** — Embeds document chunks using Ollama embeddings and stores them for retrieval.
- 💬 **Question Answering** — Ask questions about your documents and receive answers using the Mistral model (Ollama).
- 🎯 **Prompt Routing** — Smart prompts are generated based on the intent (e.g., summarization, keyword extraction).
- 📄 **Source Snippets** — Display and highlight the actual document passage used to generate each answer.
- 🖍️ **Visual Highlighting** — Answer snippets are located and highlighted in the original PDF.
- 📊 **Table Extraction** — Automatically detect and display tables using pdfplumber.
- 📈 **Chart Extraction** — Extract embedded charts/images from documents using PyMuPDF.
- 🧠 **Sentiment Analysis (Page-wise)** — Analyze sentiment for each page using TextBlob with summary and CSV export.
- 🧼 **Clean Interactive UI** — Onboarding experience, emoji-enhanced UX, collapsible sections, and dynamic controls.

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — Interactive web app framework.
- **LangChain** — RAG pipeline and document chain logic.
- **Ollama** — Local model inference (Mistral).
- **FAISS** — Fast approximate nearest neighbor search for vector DB.
- **TextBlob** — Sentiment analysis.
- **pdfplumber / PyMuPDF** — PDF parsing and visual extraction.
- **spaCy** — (NER ready, not wired in yet)

---

## 📂 Project Structure

```
├── app.py # Main Streamlit application 
├── utils/ # Utility scripts for core functionalities 
│ ├── pdf_loader.py # PDF parsing, metadata, chart & table extraction 
│ ├── chunking.py # Document splitting logic 
│ ├── vector_store.py # FAISS vector store creation & loading 
│ ├── prompt_router.py # Smart query prompt routing 
│ ├── rag_chain.py # LangChain QA chain setup with Ollama 
│ ├── sentiment_analysis.py# Page-wise sentiment analysis 
│ ├── pdf_highlight.py # Visual Q&A: highlight source snippets in PDFs 
│ ├── classify.py # (Ready) Document classification via LLM 
│ ├── ner.py # (Ready) Named entity recognition using spaCy 
├── uploaded_pdfs/ # Directory for storing uploaded PDF files 
├── my_faiss_index/ # Directory for storing the FAISS vector index 
└── README.md # Project documentation
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com) installed and running locally
- Streamlit

### Setup Steps

```bash
# 1. Clone the repo
- git clone https://github.com/rishabh15b/docuquery.git
- cd docuquery

# 2. Set up virtual environment
- python -m venv venv
- source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
- pip install -r requirements.txt

# 4. Pull the Ollama Mistral model
- ollama pull mistral

# 5. Run the app
- streamlit run app.py

# 6. (In separate terminal) Start Ollama server
- ollama serve

# 7. Open the app in your browser
- Go to http://localhost:8501

---

## 🧠 Usage

1. Upload PDFs from the sidebar.
2. Configure chunk size & overlap (optional).
3. Choose optional features: charts, tables, sentiment, highlighting.
4. Ask questions using natural language.
5. View answers with highlighted source, sentiment charts, and extracted data.
6. Download sentiment results (CSV) if enabled.

---

## 🌟 Current Model: Mistral (via Ollama)

- Runs locally on CPU or GPU
- Supports long-context document Q&A
- Great reasoning performance with low latency
- Ideal for personal or internal use without API keys

---

## 📌 Next Up (Planned Features)

- 🔍 **Named Entity Recognition (NER)** → show people, orgs, etc.
- 🧾 **Document Classifier** → auto-tag as resume, invoice, research paper
- 📘 **Section Summarizer & Navigator** → quick jump to abstract, conclusion
- 🌐 **Multilingual Support**
- 🔄 **Model Switching** → Ollama / GPT-4 / Claude
- 📊 **Dashboard Tabs** → Sentiment, Keywords, Entities, Summary

---

## 📄 License

- This project is licensed under the MIT License.

---

## 👨‍💻 Author

- Developed by [Rishabh Balaiwar](https://github.com/rishabh15b). Feel free to reach out for questions or collaboration opportunities!

---

## 📞 Contact

- For support or inquiries, contact me at:
- Email: <rbalaiwar@gmail.com>
- GitHub: [Your GitHub Profile](https://github.com/rishabh15b)

