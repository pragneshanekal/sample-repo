import os
from typing import Dict, List, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define state schema
class GraphState(TypedDict):
    """State schema for code generation graph."""
    requirements: str
    code_solution: str
    explanation: str
    messages: List[str]
    error: str

# Define output schema
class CodeSolution(BaseModel):
    """Schema for code generation output."""
    code: str = Field(description="Generated code with documentation")
    explanation: str = Field(description="Detailed explanation of implementation")
    imports: str = Field(description="Required import statements")

def get_llm(api_key: str) -> ChatOpenAI:
    """Initialize ChatOpenAI with provided API key."""
    return ChatOpenAI(
        temperature=0.1,
        model="gpt-4",
        api_key=api_key
    )

def create_code_generation_chain(llm: ChatOpenAI):
    """Create the code generation chain with proper prompting."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Python programmer. Generate well-documented code based on the requirements.
        Include comprehensive docstrings and inline comments. Structure your response with:
        1. Import statements
        2. Documented code implementation
        3. Detailed explanation of the approach"""),
        ("user", "{requirements}")
    ])
    return prompt | llm.with_structured_output(CodeSolution)

def generate_code(state: GraphState) -> Dict:
    """Node for generating code based on requirements."""
    try:
        logger.info("Generating code from requirements")
        llm = get_llm(state.get("api_key", ""))
        chain = create_code_generation_chain(llm)
        solution = chain.invoke({"requirements": state["requirements"]})
        return {
            "code_solution": solution.code,
            "explanation": solution.explanation,
            "error": ""
        }
    except Exception as e:
        logger.error(f"Error in code generation: {str(e)}")
        return {"error": str(e)}

def validate_code(state: GraphState) -> str:
    """Node for validating generated code."""
    if state["error"]:
        return "error"
    return "end"

def create_graph(api_key: str):
    """Create and configure the LangGraph workflow."""
    # Initialize graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("generate", generate_code)
    
    # Add edges
    workflow.set_entry_point("generate")
    workflow.add_conditional_edges(
        "generate",
        validate_code,
        {
            "end": END,
            "error": "generate"
        }
    )
    
    return workflow.compile()

def process_requirements(requirements: str, api_key: str) -> Dict:
    """Process programming requirements and generate code solution."""
    try:
        # Initialize graph with state
        graph = create_graph(api_key)
        
        # Execute graph
        result = graph.invoke({
            "requirements": requirements,
            "code_solution": "",
            "explanation": "",
            "messages": [],
            "error": "",
            "api_key": api_key
        })
        
        return {
            "code": result["code_solution"],
            "explanation": result["explanation"],
            "error": result["error"]
        }
    except Exception as e:
        logger.error(f"Error processing requirements: {str(e)}")
        return {"error": str(e)}