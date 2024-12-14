# LangGraph PDF-Based RAG Agent

## Project Description
The **LangGraph PDF-Based RAG Agent** is a local application designed to assist users in retrieving information from PDF documents. By leveraging semantic embedding generation and contextual response generation, this agent allows users to upload PDF files, query them using natural language, and receive informative responses that cite the sources of the information.

### Key Features
- **PDF Loading and Processing**: Users can upload and process PDF documents from their local storage.
- **Semantic Embedding Generation**: The agent generates and stores embeddings locally for efficient reuse, avoiding the need for reprocessing.
- **Semantic Search**: A semantic search index is built using the embeddings, enabling natural language queries to retrieve relevant passages from the PDFs.
- **Contextual Response Generation**: The agent combines retrieved passages with language model capabilities to generate clear and informative responses, citing sources including the PDF file name and page number.

## Code Structure

```
.
├── frontend.py         # Streamlit frontend for user interaction
└── backend.py          # Backend logic for processing PDFs and generating responses

```

### Key Files
- **frontend.py**: This file contains the Streamlit application that allows users to upload PDF documents, enter queries, and view responses.
- **backend.py**: This file implements the core logic of the PDF RAG agent, including PDF processing, embedding generation, semantic search, and response generation.

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- An OpenAI API key (for using OpenAI models)

### Installation Steps
1. **Clone the repository**:
   <bash>
   git clone https://github.com/yourusername/langgraph-pdf-rag-agent.git
   cd langgraph-pdf-rag-agent
   </bash>

2. **Set up the development environment**:
   It is recommended to use a virtual environment. You can create one using:
   <bash>
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   </bash>

3. **Install dependencies**:
   Install the required packages using pip:
   <bash>
   pip install -r requirements.txt
   </bash>

4. **Run the application**:
   Start the Streamlit application:
   <bash>
   streamlit run frontend.py
   </bash>

## Dependencies
- `langgraph==0.2.53`
- `streamlit`
- `chromadb`
- `langchain_community`
- `langchain_openai`
- `langchain_core`
- `typing_extensions`

## Configuration Instructions
1. Open the Streamlit application in your web browser.
2. In the sidebar, enter your OpenAI API key to enable the agent's functionality.

## Usage Examples
1. **Upload PDF Documents**: Use the file uploader to select and upload one or more PDF files.
2. **Ask Questions**: Enter a question related to the content of the uploaded PDFs in the provided text input field.
3. **View Responses**: After processing, the agent will display the generated response along with the sources cited.

## Troubleshooting Tips
- If you encounter issues with PDF processing, ensure that the files are in a valid PDF format.
- Make sure your OpenAI API key is correctly entered in the sidebar.
- If the application fails to start, check for any missing dependencies or errors in the console output.

This README provides a comprehensive overview of the LangGraph PDF-Based RAG Agent, guiding users through setup, usage, and troubleshooting.