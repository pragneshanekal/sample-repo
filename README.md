# LangGraph PDF-Based RAG Agent

## Project Description
The LangGraph PDF-Based RAG Agent is a local application designed to assist users in retrieving information from PDF documents. By leveraging semantic search and contextual response generation, this agent allows users to upload PDFs, query them using natural language, and receive informative responses with proper citations. This project addresses the challenge of efficiently extracting relevant information from large volumes of PDF documents, making it easier for users to find the information they need.

## Key Features
- **PDF Loading and Processing**: Users can upload and process multiple PDF documents.
- **Semantic Embedding Generation**: Efficiently generates and stores embeddings for quick retrieval.
- **Semantic Search**: Enables natural language queries to find relevant passages in the PDFs.
- **Contextual Response Generation**: Combines retrieved passages with language model capabilities to provide clear and informative answers, including citations.

## Code Structure

```
project-root/
│
├── frontend.py          # Streamlit frontend for user interaction
├── backend.py           # Backend logic for processing PDFs and generating responses
├── requirements.txt     # List of dependencies required for the project
└── README.md            # Project documentation

```

### Key Files and Modules
- **frontend.py**: Contains the Streamlit application code for user interface, including file upload and query input.
- **backend.py**: Implements the `PDFRagAgent` class, which handles PDF processing, embedding generation, semantic search, and response generation.
- **requirements.txt**: Lists all the necessary Python packages to run the application.

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- An OpenAI API key (for using OpenAI\'s language models)

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
   <bash>
   pip install -r requirements.txt
   </bash>

4. **Run the application**:
   <bash>
   streamlit run frontend.py
   </bash>

## Dependencies
- `langgraph==0.2.53`
- `streamlit`
- `langchain_community`
- `langchain`
- `langchain_openai`
- `langchain_core`
- `tempfile`
- `os`
- `typing`
- `pathlib`

## Configuration Instructions
1. Open the application in your web browser (usually at `http://localhost:8501`).
2. In the sidebar, enter your OpenAI API key to enable the agent\'s functionality.

## Usage Examples
1. **Upload PDF Documents**: Use the file uploader to select and upload one or more PDF files.
2. **Ask Questions**: After processing the PDFs, enter your question in the provided text input field and click "Process PDFs" to retrieve relevant information.
3. **View Responses**: The application will display the generated response along with the sources cited.

## Troubleshooting Tips
- If you encounter issues with PDF processing, ensure that the files are not corrupted and are in the correct format.
- Make sure your OpenAI API key is valid and has the necessary permissions.
- If the application fails to start, check for any missing dependencies or errors in the console output.

This README provides a comprehensive overview of the LangGraph PDF-Based RAG Agent, guiding users through setup, usage, and troubleshooting.