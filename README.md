# PDF-based RAG Agent

## Project Description
The PDF-based RAG (Retrieval-Augmented Generation) Agent is a web application designed to process PDF documents, extract relevant information, and provide contextual responses to user queries. By leveraging OpenAI\'s language models and advanced embedding techniques, this application enables users to interact with the content of PDF files in a meaningful way, making it easier to retrieve specific information and citations.

### Key Features
- Upload and process PDF documents.
- Extract text and relevant information from PDFs.
- Ask questions about the document and receive contextual responses.
- Provide citations for the information retrieved.

## Code Structure

```
project-root/
│
├── frontend.py          # Streamlit frontend for user interaction
├── backend.py           # Backend logic for processing PDFs and generating responses
└── requirements.txt     # List of dependencies required for the project

```

### Key Files and Modules
- **frontend.py**: Contains the Streamlit application code that handles user input, file uploads, and displays responses.
- **backend.py**: Implements the logic for processing PDF files, generating embeddings, and retrieving answers based on user queries.
- **requirements.txt**: Lists the necessary Python packages to run the application.

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- An OpenAI API key (for accessing OpenAI\'s language models)

### Installation Steps
1. **Clone the repository**:
   <bash>
   git clone <repository-url>
   cd <repository-directory>
   </bash>

2. **Set up the development environment** (optional but recommended):
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
- `os`
- `pdfplumber`
- `langchain`

## Configuration Instructions
- Open the application in your web browser after running the Streamlit command.
- Enter your OpenAI API key in the sidebar to enable the application to access OpenAI\'s models.

## Usage Examples
1. Upload a PDF document using the file uploader.
2. After the PDF is processed, enter a question related to the content of the document.
3. Click the "Get Response" button to receive an answer along with citations.

## Troubleshooting Tips
- If you encounter issues with file uploads, ensure that the PDF file is not corrupted and is in the correct format.
- Make sure your OpenAI API key is valid and has the necessary permissions.
- If the application does not start, check for any error messages in the terminal and ensure all dependencies are installed correctly.