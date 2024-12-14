import os
import tempfile
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from typing_extensions import TypedDict

import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

@dataclass
class Document:
    """Represents a processed document with its content and metadata."""
    content: str
    metadata: Dict[str, Any]

class GraphState(TypedDict):
    """State maintained between nodes in the graph."""
    query: str
    documents: List[Document]
    response: str
    sources: List[str]

class PDFRagAgent:
    def __init__(self):
        """Initialize the PDF RAG Agent with necessary components."""
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Initialize ChromaDB
        self.vector_store = Chroma(
            collection_name="pdf_rag",
            embedding_function=self.embeddings
        )
        
        # Initialize LangGraph
        self.graph = self._build_graph()
        self.app = self.graph.compile()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow for RAG."""
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("retrieve", self._retrieve_documents)
        workflow.add_node("generate", self._generate_response)
        
        # Build graph
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow

    def _retrieve_documents(self, state: GraphState) -> GraphState:
        """Retrieve relevant documents based on the query."""
        docs = self.vector_store.similarity_search(
            state["query"],
            k=3
        )
        
        documents = [
            Document(
                content=doc.page_content,
                metadata=doc.metadata
            ) for doc in docs
        ]
        
        return {"query": state["query"], "documents": documents}

    def _generate_response(self, state: GraphState) -> GraphState:
        """Generate a response using retrieved documents."""
        context = "\n\n".join([doc.content for doc in state["documents"]])
        
        messages = [
            SystemMessage(content="You are a helpful assistant that answers questions based on the provided context. Always be factual and cite your sources."),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion: {state['query']}")
        ]
        
        response = self.llm.invoke(messages)
        
        sources = [
            f"File: {doc.metadata['source']}, Page: {doc.metadata['page']}"
            for doc in state["documents"]
        ]
        
        return {
            "query": state["query"],
            "documents": state["documents"],
            "response": response.content,
            "sources": sources
        }

    def process_pdf(self, file) -> None:
        """Process a PDF file and store its embeddings."""
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file.getvalue())
            file_path = tmp_file.name
        
        try:
            # Load and process PDF
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(pages)
            
            # Add to vector store
            self.vector_store.add_documents(chunks)
            
        finally:
            # Cleanup temporary file
            os.unlink(file_path)

    def query(self, question: str) -> Tuple[str, List[str]]:
        """Query the RAG system with a question."""
        result = self.app.invoke({"query": question})
        return result["response"], result["sources"]