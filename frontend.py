import streamlit as st
import os
from backend import process_pdf, get_response

# Sidebar for OpenAI API Key
st.sidebar.title('Configuration')
openai_api_key = st.sidebar.text_input('Enter your OpenAI API Key')

if openai_api_key:
    os.environ['OPENAI_API_KEY'] = openai_api_key

st.title('PDF-based RAG Agent')

# File uploader for PDF documents
uploaded_file = st.file_uploader('Upload PDF Document', type='pdf')

if uploaded_file is not None:
    # Process the PDF and extract relevant information
    pdf_text = process_pdf(uploaded_file)
    st.write('Extracted Text:')
    st.write(pdf_text)

    # User query input
    user_query = st.text_input('Ask a question about the document:')

    if st.button('Get Response'):
        if user_query:
            response, citations = get_response(user_query, pdf_text)
            st.write('Response:')
            st.write(response)
            st.write('Citations:')
            st.write(citations)
        else:
            st.warning('Please enter a question.')