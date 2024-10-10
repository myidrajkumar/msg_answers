"""Loading the LLMs"""

from langchain_ollama import ChatOllama


def initialize_llm():
    """Initialize the llm"""
    llm = ChatOllama(model="llama3.2:latest", streaming=True)
    return llm
