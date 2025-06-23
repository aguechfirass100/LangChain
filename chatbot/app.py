import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# import google.generativeai as genai
# from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
# LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries"),
        ("user", "Question: {question}"),
    ]
)

# Streamlit Framework
st.title("Langchain Demo with OpenAI API")
input_text = st.text_input("Search the topic you want")

# LLMs
llm_openai = ChatOpenAI(model="gemini-1.5-turbo")
# llm_gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
# model = genai.GenerativeModel("gemini-1.5-flash")

output_paerser = StrOutputParser()
chain = prompt | llm_openai | output_paerser

if input_text:
    st.write(chain.invoke({"question": input_text}))
