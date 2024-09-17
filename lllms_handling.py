"""Loading the LLMs"""

from langchain_ollama import ChatOllama


def initialize_llm():
    """Initialize the llm"""
    llm = ChatOllama(model="llama3.1:latest", temperature=0.8)
    return llm
