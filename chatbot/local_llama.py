import os

import streamlit as st
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries"),
        ("user", "Question: {question}"),
    ]
)

# Streamlit Framework
st.title("Langchain Demo with Ollama - Local LLMs - gemma3:1b")
input_text = st.text_input("Search the topic you want")

# Ollama LLM
llm = Ollama(model="gemma3:1b")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))
