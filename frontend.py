import streamlit as st
from backend import PDFRagAgent

st.set_page_config(page_title="PDF RAG Agent", layout="wide")

# Initialize session state
if "rag_agent" not in st.session_state:
    st.session_state.rag_agent = None

# Sidebar for API key
with st.sidebar:
    st.title("Configuration")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    if api_key:
        st.session_state.rag_agent = PDFRagAgent(api_key)

st.title("PDF RAG Agent")

# File uploader
uploaded_files = st.file_uploader("Upload PDF Documents", type="pdf", accept_multiple_files=True)

if uploaded_files and st.session_state.rag_agent:
    if st.button("Process PDFs"):
        with st.spinner("Processing PDFs..."):
            for pdf_file in uploaded_files:
                st.session_state.rag_agent.process_pdf(pdf_file)
        st.success("PDFs processed successfully!")

    # Query interface
    st.subheader("Ask Questions")
    user_query = st.text_input("Enter your question about the documents")
    
    if user_query:
        with st.spinner("Generating response..."):
            response = st.session_state.rag_agent.query(user_query)
            
        st.markdown("### Response")
        st.write(response["answer"])
        
        st.markdown("### Sources")
        for source in response["sources"]:
            st.markdown(f"- {source}")
        
elif not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to continue.")
elif not uploaded_files:
    st.info("Please upload PDF documents to begin.")