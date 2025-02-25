import os
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key securely
groq_api_key = os.getenv("GROQ_API_KEY")


# Initialize the Groq API key and model
groq_api_key = groq_api_key  # Replace with your Groq API key
llm = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

def analyze_page_with_groq(content):
    # Create a prompt that combines the context and the page content
    prompt = f"""
                You are an expert in web design and UX. Analyze the page content for e-commerce websites and suggest improvements. 
                Additionally, provide insights on:  
                - Website traffic trends (organic vs. paid, bounce rate, user engagement)  
                - SEO improvements (keyword analysis, backlinks, SEMrush insights)  
                - Page loading speed optimization  
                - Search functionality for guest users  
                - Website length and readability  
                - Mobile vs. desktop usability  

            Page Content:{content}"""
    
    # Generate response from the model, wrap the prompt in a HumanMessage object
    response = llm.generate([[HumanMessage(content=prompt)]])
    return response.generations[0][0].text  # Extract the response text

def load_and_analyze_url(url):
    loader = WebBaseLoader(url)
    try:
        documents = loader.load_and_split()
        if documents:
            page_content = documents[0].page_content
            suggestions = analyze_page_with_groq(page_content)
            return suggestions
        else:
            return "Failed to load content from the URL. Please check the URL and try again."
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title("Website Analysis Tool")
st.write("Analyze e-commerce websites for design and UX improvements.")

# Input field for the URL
url = st.text_input("Enter the URL of the website:", "")

# Submit button
if st.button("Submit"):
    if url:
        with st.spinner("Analyzing the website..."):
            suggestions = load_and_analyze_url(url)
        # Display the analysis suggestions
        st.subheader("Website Analysis Suggestions:")
        st.write(suggestions)
    else:
        st.warning("Please enter a valid URL.")
