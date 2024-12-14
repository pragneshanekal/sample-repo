import streamlit as st
from backend import PDFRagAgent
import os

st.set_page_config(page_title="PDF RAG Agent", layout="wide")

# Initialize session state
if "rag_agent" not in st.session_state:
    st.session_state.rag_agent = None

# Sidebar for API key
with st.sidebar:
    st.title("Configuration")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        if st.session_state.rag_agent is None:
            st.session_state.rag_agent = PDFRagAgent()
        st.success("API Key set successfully!")

# Main content
st.title("PDF RAG Agent")

# File uploader
uploaded_files = st.file_uploader(
    "Upload PDF Documents", 
    type=["pdf"], 
    accept_multiple_files=True
)

if uploaded_files and api_key:
    if st.button("Process PDFs"):
        with st.spinner("Processing PDF documents..."):
            for file in uploaded_files:
                st.session_state.rag_agent.process_pdf(file)
        st.success("PDFs processed successfully!")

    # Query interface
    st.subheader("Ask Questions")
    query = st.text_input("Enter your question about the documents")
    
    if query:
        with st.spinner("Generating response..."):
            response, sources = st.session_state.rag_agent.query(query)
            
            # Display response
            st.markdown("### Response")
            st.write(response)
            
            # Display sources
            st.markdown("### Sources")
            for source in sources:
                st.markdown(f"- {source}")

elif not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to continue.")
else:
    st.info("Please upload PDF documents to begin.")