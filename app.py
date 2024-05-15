# Q&A Chatbot
from langchain.llms import OpenAI
from dotenv import load_dotenv
import streamlit as st
import os

# Load environment variables from .env
load_dotenv()

# Initialize the OpenAI model outside the Streamlit callback
llm = OpenAI(api_key=os.getenv("OPEN_API_KEY"), model_name="gpt-3.5-turbo", temperature=0.5)

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Langchain Application")

# Input text box for user input
input_text = st.text_input("Input: ", key="input")

# If "Ask the question" button is clicked
if st.button("Ask the question"):
    # Get response from OpenAI model
    response = llm(input_text)
    # Display the response
    st.subheader("The Response is")
    st.write(response)
