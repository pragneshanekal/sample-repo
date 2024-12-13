import os
import pdfplumber
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.document_loaders import DocumentLoader
from langchain.text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Function to process PDF and extract text
def process_pdf(uploaded_file):
    """Process the uploaded PDF file and extract text."""
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

# Function to get response from the RAG agent
def get_response(user_query, pdf_text):
    """Get a response from the RAG agent based on the user query and extracted PDF text."""
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    doc_splits = text_splitter.split_documents([pdf_text])
    vectorstore = Chroma.from_documents(doc_splits, embeddings)

    # Create retriever
    retriever = vectorstore.as_retriever()

    # Create RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAIEmbeddings(),
        chain_type='stuff',
        retriever=retriever
    )

    # Get response and citations
    response = qa_chain.run(user_query)
    citations = [doc.metadata['source'] for doc in retriever.get_relevant_documents(user_query)]
    return response, citations

# Define the LangGraph workflow
graph = StateGraph(AgentState)

# Add nodes and edges for the workflow
# Initialize nodes
graph.add_node('process_pdf', process_pdf)
graph.add_node('get_response', get_response)

# Add edges
graph.add_edge(START, 'process_pdf')
graph.add_edge('process_pdf', 'get_response')
graph.add_edge('get_response', END)

# Compile the graph with memory saver
app = graph.compile(checkpointer=MemorySaver())