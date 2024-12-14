import streamlit as st
from backend import process_requirements

def main():
    st.set_page_config(page_title="Code Generation Assistant", layout="wide")
    
    # Sidebar for API key
    with st.sidebar:
        st.title("Configuration")
        api_key = st.text_input("Enter OpenAI API Key", type="password")
        st.markdown("---")
    
    # Main content
    st.title("Code Generation Assistant")
    st.markdown("""
    This assistant helps you generate well-documented Python code based on your requirements.
    Please provide detailed specifications for your programming needs.
    """
    )
    
    # Input section
    requirements = st.text_area(
        "Enter Programming Requirements",
        height=200,
        placeholder="Describe the functionality you need..."
    )
    
    if st.button("Generate Code") and requirements and api_key:
        with st.spinner("Generating code..."):
            result = process_requirements(requirements, api_key)
            
            if result.get("error"):
                st.error(f"Error: {result['error']}")
            else:
                # Display generated code
                st.subheader("Generated Code")
                st.code(result["code"], language="python")
                
                # Display explanation
                st.subheader("Implementation Explanation")
                st.markdown(result["explanation"])
    
    elif st.button("Generate Code"):
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        if not requirements:
            st.error("Please enter your programming requirements.")

if __name__ == "__main__":
    main()