import requests
import streamlit as st


def get_openai_response(input_text):
    response = requests.post(
        "http://localhost:8000/poem/invoke", json={"input": {"topic": input_text}}
    )

    return response.json()["output"]["content"]


def get_ollama_response(input_text):
    response = requests.post(
        "http://localhost:8000/poem/invoke", json={"input": {"topic": input_text}}
    )

    return response.json()["output"]


# Streamlit Framework
st.title("Langchain Demo with OpenAI and Ollama")
input_text = st.text_input("Write an essay on")
input_text1 = st.text_input("Write a poem on")

if input_text:
    st.write("OpenAI Response:")
    st.write(get_openai_response(input_text))

if input_text1:
    st.write("Ollama Response:")
    st.write(get_ollama_response(input_text1))
