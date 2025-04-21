import streamlit as st
import os
import shutil
import pandas as pd
from PIL import Image
import io
import matplotlib.pyplot as plt

from utils.pdf_loader import load_all_pdfs, extract_metadata, extract_tables, extract_charts
from utils.chunking import split_docs
from utils.vector_store import create_store, load_store
from utils.prompt_router import get_smart_prompt
from utils.rag_chain import get_qa_chain
from utils.sentiment_analysis import analyze_sentiment_by_page
from utils.pdf_highlight import find_snippet_location, render_highlighted_page
from utils.ner import extract_named_entities

UPLOAD_DIR = "uploaded_pdfs"
VECTOR_DIR = "my_faiss_index"

if 'history' not in st.session_state:
    st.session_state.history = []
if 'db' not in st.session_state:
    st.session_state.db = None
if 'visited' not in st.session_state:
    st.session_state.visited = False

st.set_page_config(page_title="📄 DocuQuery", layout="wide")

# 👋 Onboarding Message
if not st.session_state.visited:
    with st.expander("👋 Welcome to DocuQuery", expanded=True):
        st.markdown("""
        Upload your PDFs and ask natural questions. DocuQuery will use AI to find answers,
        extract data, analyze tone, and more.

        **Example questions:**
        - What is the document about?
        - Who authored this?
        - Summarize the content.
        """)
    st.session_state.visited = True

# Sidebar Inputs
with st.sidebar:
    st.header("📁 Upload PDF Files")
    uploaded_files = st.file_uploader("Select PDF(s)", type=["pdf"], accept_multiple_files=True)
    st.markdown("---")

    st.header("⚙️ Chunking Settings")
    chunk_size = st.slider("Chunk Size", 500, 2000, 800, 100)
    overlap = st.slider("Chunk Overlap", 0, 500, 200, 50)

    st.header("🧠 Analysis Options")
    analyze_tables = st.checkbox("📊 Extract Tables")
    analyze_charts = st.checkbox("📈 Extract Charts")
    perform_sentiment_analysis = st.checkbox("🧠 Sentiment Analysis")
    perform_ner = st.checkbox("🔎 Named Entity Recognition")
    enable_visual_qa = st.checkbox("🖍️ Visual Highlighting", value=True)

    if st.button("🧹 Clear Uploaded Files"):
        shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
        st.success("Cleared uploaded files.")

# Handle Uploads
pdf_paths = []
if uploaded_files:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    for file in uploaded_files:
        path = os.path.join(UPLOAD_DIR, file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        pdf_paths.append(path)
    st.sidebar.success(f"Uploaded {len(uploaded_files)} file(s).")

# Title
st.markdown("### 🦙 DocuQuery")
st.markdown("_Your AI assistant for smarter PDF understanding_")

# Build or Load Vector Store
if pdf_paths:
    if os.path.exists(VECTOR_DIR):
        shutil.rmtree(VECTOR_DIR)
    raw_docs = load_all_pdfs(pdf_paths)
    chunks = split_docs(raw_docs, chunk_size=chunk_size, overlap=overlap)
    st.session_state.db = create_store(chunks, VECTOR_DIR)
else:
    if st.session_state.db is None:
        try:
            st.session_state.db = load_store(VECTOR_DIR)
        except FileNotFoundError:
            st.warning("Please upload at least one PDF to begin.")
            st.stop()

qa_chain = get_qa_chain(st.session_state.db)

# 💬 Question Interface
st.subheader("💬 Ask a Question")
query = st.text_input("Enter your question:")
if st.button("🔍 Get Answer") and query:
    with st.spinner("Generating answer..."):
        smart_query = get_smart_prompt(query)
        try:
            result = qa_chain({"query": smart_query})
            st.session_state.history.append({"query": query, "answer": result["result"]})

            st.markdown("### 📚 Answer:")
            max_chars = 1200
            if len(result["result"]) > max_chars:
                display_text = result["result"][:max_chars] + "..._(truncated)_"
            else:
                display_text = result["result"]
            st.markdown(display_text)

            if perform_ner:
                st.markdown("### 🔎 Named Entities")
                entities = extract_named_entities([result["result"]])
                if entities and entities[0]:
                    for ent in entities[0]:
                        st.markdown(f"- **{ent['text']}** ({ent['label']})")
                else:
                    st.info("No named entities detected in the answer.")

            if enable_visual_qa:
                with st.expander("📄 Source Snippets"):
                    for i, doc in enumerate(result["source_documents"]):
                        page_num = doc.metadata.get("page", "?")
                        st.markdown(f"**Source {i+1} (Page {page_num}):**")
                        st.write(doc.page_content)

                        snippet_info = find_snippet_location(doc.page_content[:100], doc.metadata["source"])
                        if snippet_info:
                            image_bytes = render_highlighted_page(
                                snippet_info["file_path"], snippet_info["page"], snippet_info["bbox"]
                            )
                            image = Image.open(io.BytesIO(image_bytes))
                            st.image(image, caption=f"Highlighted Snippet (Page {snippet_info['page'] + 1})")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# 🧠 Sentiment Analysis
if perform_sentiment_analysis and pdf_paths:
    st.header("🧠 Sentiment Analysis (Page-wise)")
    sentiment_data = analyze_sentiment_by_page(pdf_paths)

    for doc_result in sentiment_data:
        doc_name = os.path.basename(doc_result["file"])
        page_sentiments = doc_result["pages"]

        with st.expander(f"📄 Sentiment Insights for: {doc_name}"):
            avg_polarity = sum(p["polarity"] for p in page_sentiments) / len(page_sentiments)
            avg_subjectivity = sum(p["subjectivity"] for p in page_sentiments) / len(page_sentiments)
            overall_sentiment = "Positive" if avg_polarity > 0.1 else "Negative" if avg_polarity < -0.1 else "Neutral"
            sentiment_emoji = "😄" if overall_sentiment == "Positive" else "😞" if overall_sentiment == "Negative" else "😐"

            st.markdown(f"""
            <div style='padding: 0.5rem; background-color: #f0f2f6; border-radius: 10px;'>
            <b>📄 File:</b> {doc_name}<br>
            <b>📊 Overall Sentiment:</b> {overall_sentiment} {sentiment_emoji}<br>
            <b>📈 Avg Polarity:</b> {avg_polarity:.2f} | <b>🌗 Avg Subjectivity:</b> {avg_subjectivity:.2f}
            </div>
            """, unsafe_allow_html=True)

            flagged = [p for p in page_sentiments if abs(p["polarity"]) > 0.3]
            if flagged:
                st.markdown("**⚠️ Pages with strong sentiment:** " + ", ".join([f"Page {p['page']}" for p in flagged]))
            else:
                st.markdown("Sentiment is mostly neutral across pages.")

            st.markdown("""
            **Legend:**
            - 📈 **Polarity**: Sentiment tone (−1 = negative, +1 = positive)
            - 🌗 **Subjectivity**: Opinion level (0 = objective, 1 = subjective)
            """)

            fig, ax = plt.subplots()
            pages = [p["page"] for p in page_sentiments]
            polarities = [p["polarity"] for p in page_sentiments]
            subjectivities = [p["subjectivity"] for p in page_sentiments]

            ax.plot(pages, polarities, marker="o", label="📈 Polarity")
            ax.plot(pages, subjectivities, marker="x", linestyle="--", label="🌗 Subjectivity")
            ax.axhline(0, color="gray", linestyle=":", linewidth=1)
            ax.set_xlabel("Page")
            ax.set_ylabel("Score")
            ax.set_title("Sentiment Scores per Page")
            ax.legend()

            st.pyplot(fig)

            csv_data = pd.DataFrame(page_sentiments).to_csv(index=False)
            st.download_button("📥 Download Sentiment Data as CSV", csv_data, file_name=f"{doc_name}_sentiment.csv")

            if avg_polarity > 0.1:
                st.success("✅ The document overall carries a positive tone.")
            elif avg_polarity < -0.1:
                st.error("⚠️ The document contains mostly negative sentiment.")
            else:
                st.info("ℹ️ The sentiment throughout the document is mostly neutral or objective.")

# 📊 Tables & Charts
if analyze_tables:
    st.subheader("📊 Extracted Tables")
    tables = extract_tables(pdf_paths)
    if tables:
        for i, table in enumerate(tables):
            st.markdown(f"**Table {i+1}:**")
            try:
                df = pd.DataFrame(table[1:], columns=table[0])
                st.dataframe(df, use_container_width=True)
            except:
                st.write(table)
    else:
        st.info("No tables found in the uploaded documents.")

if analyze_charts:
    st.subheader("📈 Extracted Charts")
    charts = extract_charts(pdf_paths)
    if charts:
        for i, chart in enumerate(charts):
            image = Image.open(io.BytesIO(chart))
            width, height = image.size
            max_width = 600
            scale = max_width / width if width > max_width else 1.0
            resized_image = image.resize((int(width * scale), int(height * scale)))
            st.image(resized_image, caption=f"Chart {i+1}", use_column_width=False)
    else:
        st.info("No charts found in the uploaded documents.")