import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
    title="LangServe API",
    description="API for LangServe with Ollama",
    version="1.0",
)

ollama_model = Ollama(model="gemma3:1b")

prompt = ChatPromptTemplate.from_template(
    "write me an Eminem style poem about {topic} with 100 words"
)

chain = prompt | ollama_model | StrOutputParser()


class PoemInput(BaseModel):
    topic: str


add_routes(
    app,
    chain,
    path="/poem",
    input_type=PoemInput,
    output_type=str,
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
