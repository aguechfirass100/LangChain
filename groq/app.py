import os
import time

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# from langchain_ollama import OllamaEmbeddings

load_dotenv()

## load te Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

if "vector" not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    # st.session_state.loader = WebBaseLoader("https://docs.smith.langchain.com")
    st.session_state.loader = WebBaseLoader("https://aman.ai/primers/ai/RAG/")
    st.session_state.docs = st.session_state.loader.load()

    st.session_state.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(
        st.session_state.docs,
        # st.session_state.embeddings
    )
    st.session_state.vector = FAISS.from_documents(
        st.session_state.final_documents, st.session_state.embeddings
    )

st.title("Chat Groq Demo")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="deepseek-r1-distill-llama-70b")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.
    <context>
    {context}
    </context>
    Questiobs: {input}
    """
)

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = st.session_state.vector.as_retriever()
retriever_chain = create_retrieval_chain(retriever, document_chain)

prompt = st.text_input("Input your prompt here")

if prompt:
    start = time.process_time()
    response = retriever_chain.invoke({"input": prompt})
    print("Response time: ", time.process_time() - start)
    st.write(response["answer"])

    # with a streamlit expander
    with st.expander("Document Similarity Search"):
        # find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("-------------------------------------")
