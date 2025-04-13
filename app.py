import streamlit as st
import os
import shutil
from utils.pdf_loader import load_all_pdfs, extract_metadata
from utils.chunking import split_docs
from utils.vector_store import create_store, load_store
from utils.prompt_router import get_smart_prompt
from utils.rag_chain import get_qa_chain  # Import the new function

# Constants
UPLOAD_DIR = "uploaded_pdfs"
VECTOR_DIR = "my_faiss_index"

# Initialize history in session state if not already done
if 'history' not in st.session_state:
    st.session_state.history = []

# Streamlit Page Config
st.set_page_config(page_title="📄 DOCQuery", layout="wide")

# Sidebar for Uploads and Info
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
st.title("🦙📄 DOCQuery")

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
    # Always delete old index if new files are uploaded
    if os.path.exists(VECTOR_DIR):
        shutil.rmtree(VECTOR_DIR)

    with st.spinner("🔍 Indexing uploaded documents..."):
        raw_docs = load_all_pdfs(pdf_paths)
        chunks = split_docs(raw_docs, chunk_size=chunk_size, overlap=overlap)  # Pass dynamic values here
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
        smart_query = get_smart_prompt(query)  # Dynamic query handling

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

# Display past queries and answers
if st.session_state.history:
    st.sidebar.markdown("### 📜 Query History")
    for i, entry in enumerate(st.session_state.history):
        with st.sidebar.expander(f"Query {i + 1}"):
            st.sidebar.markdown(f"**Question:** {entry['query']}")
            st.sidebar.markdown(f"**Answer:** {entry['answer']}")

    # Clear history button in the sidebar
    if st.sidebar.button("🗑️ Clear History"):
        st.session_state.history = []
        st.sidebar.success("History cleared!")

    # Export history button in the sidebar
    if st.sidebar.button("📄 Export History"):
        history_text = "\n".join([f"Q: {entry['query']}\nA: {entry['answer']}\n" for entry in st.session_state.history])
        
        # Provide download link
        if history_text:
            st.sidebar.download_button(
                label="Download History",
                data=history_text,
                file_name="query_history.txt",
                mime="text/plain"
            )
        else:
            st.sidebar.warning("No history to export.")
# Cleanup uploaded files after processing
if os.path.exists(UPLOAD_DIR):
    shutil.rmtree(UPLOAD_DIR)
    st.sidebar.success("✅ Uploaded files cleaned up.")
                  