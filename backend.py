import os
from typing import Dict, List, Optional
from pathlib import Path
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

class PDFRagAgent:
    def __init__(self, api_key: str):
        """Initialize the PDF RAG Agent with OpenAI API key."""
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vectorstore = Chroma(
            collection_name="pdf_rag",
            embedding_function=self.embeddings
        )
        self.llm = ChatOpenAI(temperature=0)
        
        # Initialize the graph
        self.graph = self._create_graph()
        
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow for RAG."""
        # Define the graph state
        workflow = StateGraph(Dict)
        
        # Define nodes
        workflow.add_node("retrieve", self._retrieve_documents)
        workflow.add_node("generate", self._generate_response)
        
        # Define edges
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()
    
    def process_pdf(self, pdf_file) -> None:
        """Process a PDF file and add it to the vector store."""
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            # Load and split the PDF
            loader = PyPDFLoader(tmp_path)
            pages = loader.load()
            
            # Add source information
            for page in pages:
                page.metadata["source"] = f"{pdf_file.name}, Page {page.metadata['page'] + 1}"
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(pages)
            
            # Add to vector store
            self.vectorstore.add_documents(chunks)
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
    
    def _retrieve_documents(self, state: Dict) -> Dict:
        """Retrieve relevant documents based on the query."""
        try:
            docs = self.vectorstore.similarity_search(
                state["query"],
                k=3
            )
            return {"documents": docs, "query": state["query"]}
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return {"documents": [], "query": state["query"]}
    
    def _generate_response(self, state: Dict) -> Dict:
        """Generate a response using retrieved documents."""
        # Create context from documents
        context = "\n\n".join(
            f"[{doc.metadata['source']}]
{doc.page_content}"
            for doc in state["documents"]
        )
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that answers questions based on the provided documents. "
                      "Include relevant source citations in your response."),
            ("human", "Context:\n\n{context}\n\nQuestion: {query}")
        ])
        
        # Generate response
        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke({
            "context": context,
            "query": state["query"]
        })
        
        # Extract sources
        sources = [doc.metadata["source"] for doc in state["documents"]]
        
        return {
            "answer": response,
            "sources": sources
        }
    
    def query(self, query: str) -> Dict:
        """Process a query through the RAG workflow."""
        return self.graph.invoke({"query": query})