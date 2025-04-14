import streamlit as st
import os
import shutil
from utils.pdf_loader import load_all_pdfs, extract_metadata, extract_tables, extract_charts
from utils.chunking import split_docs
from utils.vector_store import create_store, load_store
from utils.prompt_router import get_smart_prompt
from utils.rag_chain import get_qa_chain
from utils.sentiment_analysis import analyze_sentiment

# Constants
UPLOAD_DIR = "uploaded_pdfs"
VECTOR_DIR = "my_faiss_index"

# Initialize history in session state if not already done
if 'history' not in st.session_state:
    st.session_state.history = []

# Streamlit Page Config
st.set_page_config(page_title="📄 DOCQuery Enhanced", layout="wide")

# Sidebar for Uploads and Settings
with st.sidebar:
    st.header("📁 Upload PDF Files")
    uploaded_files = st.file_uploader("Select one or more PDF files", type=["pdf"], accept_multiple_files=True)
    st.markdown("---")
    st.markdown("🧠 This app uses a Retrieval-Augmented Generation (RAG) pipeline powered by Ollama to answer questions based on your uploaded documents.")
    st.markdown("💡 Tip: Ask questions like 'Who is the author of this document?' or 'What are the key points of the document?'")

    # Sidebar for Chunking Settings
    st.header("⚙️ Chunking Settings")
    chunk_size = st.slider("Chunk Size", min_value=500, max_value=2000, value=1000, step=100)
    overlap = st.slider("Chunk Overlap", min_value=0, max_value=500, value=200, step=50)

    # Sidebar for Analysis Features
    st.header("📊 Document Analysis Features")
    analyze_tables = st.checkbox("Extract Tables")
    analyze_charts = st.checkbox("Extract Charts")
    # perform_sentiment_analysis = st.checkbox("Perform Sentiment Analysis")

# Save uploaded files permanently
pdf_paths = []
if uploaded_files:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        pdf_paths.append(file_path)
    st.sidebar.success(f"✅ Uploaded {len(uploaded_files)} PDF(s)")

# Main App Layout
st.title("🦙📄 DOCQuery Enhanced")

# Provide Sample Questions Section on Main Page
st.markdown("### 💡 Sample Questions You Can Ask")
st.markdown("""
Here are some examples of questions you can ask about your uploaded PDFs:
- **Who is the author of this document?**
- **What are the key points discussed in the document?**
- **Summarize this document in a few sentences.**
- **List important keywords or topics from this document.**
- **Extract contact details like email or phone number from this document.**
""")

# Load or Create Vector Store
db = None
if pdf_paths:
    if os.path.exists(VECTOR_DIR):
        shutil.rmtree(VECTOR_DIR)

    with st.spinner("🔍 Indexing uploaded documents..."):
        raw_docs = load_all_pdfs(pdf_paths)
        chunks = split_docs(raw_docs, chunk_size=chunk_size, overlap=overlap)
        db = create_store(chunks, VECTOR_DIR)
        st.success("✅ Vector store created successfully.")
else:
    try:
        db = load_store(VECTOR_DIR)
        # st.success("✅ Loaded existing vector store.")
    except FileNotFoundError:
        st.warning("⚠️ Please upload at least one PDF to begin.")
        st.stop()

# Setup QA Chain using the new utility function
qa_chain = get_qa_chain(db)

# Chat Interface
st.subheader("💬 Ask a question about your documents")
query = st.text_input("Type your question here:")

if st.button("🔍 Get Answer") and query:
    with st.spinner("🧠 Generating answer..."):
        smart_query = get_smart_prompt(query)

        # Get the result from the QA chain
        try:
            result = qa_chain({"query": smart_query})
            # Append the query and result to history
            st.session_state.history.append({
                'query': query,
                'answer': result["result"]
            })

            st.markdown("### 📚 Answer:")
            st.write(result["result"])

            with st.expander("📄 Source Snippets"):
                for i, doc in enumerate(result["source_documents"]):
                    metadata = extract_metadata(doc.metadata["source"])
                    st.markdown(f"**Source {i+1}:**")
                    st.write(doc.page_content)
                    if metadata:
                        st.write(metadata)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Document Analysis Features (Tables, Charts, Sentiment Analysis)
if analyze_tables:
    st.header("📊 Extracted Tables")
    tables = extract_tables(pdf_paths)
    if tables:
        for i, table in enumerate(tables):
            st.markdown(f"**Table {i+1}:**")
            st.write(table)
    else:
        st.warning("No tables found in the uploaded documents.")

if analyze_charts:
    st.header("📈 Extracted Charts")
    charts = extract_charts(pdf_paths)
    if charts:
        for i, chart in enumerate(charts):
            st.image(chart, caption=f"Chart {i+1}")
    else:
        st.warning("No charts found in the uploaded documents.")
        
# Perform sentiment analysis if the checkbox is selected
# if perform_sentiment_analysis:
#     st.header("🧠 Sentiment Analysis")
#     sentiment_results = analyze_sentiment(pdf_paths)  # Call the actual function
#     for i, sentiment in enumerate(sentiment_results):
#         doc_name = os.path.basename(pdf_paths[i])
#         polarity = sentiment["polarity"]
#         subjectivity = sentiment["subjectivity"]
#         sentiment_label = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
#         st.markdown(f"**Document:** {doc_name}")
#         st.markdown(f"- **Sentiment:** {sentiment_label}")
#         st.markdown(f"- **Polarity:** {polarity:.2f}")
#         st.markdown(f"- **Subjectivity:** {subjectivity:.2f}")

# Display past queries and answers
if st.session_state.history:
    with st.sidebar:
        st.markdown("### 📜 Query History")
        for i, entry in enumerate(st.session_state.history):
            with st.expander(f"Query {i + 1}"):
                st.markdown(f"**Question:** {entry['query']}")
                st.markdown(f"**Answer:** {entry['answer']}")

# Cleanup uploaded files after processing (optional)
if os.path.exists(UPLOAD_DIR):
    shutil.rmtree(UPLOAD_DIR)
    st.sidebar.success("✅ Temporary files cleaned up.")            