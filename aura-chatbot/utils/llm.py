import os
from langchain_groq import ChatGroq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if GROQ_API_KEY == "":
    raise Exception("API Key not registered")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,  # type: ignore
)
