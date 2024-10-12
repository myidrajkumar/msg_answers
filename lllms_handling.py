"""Loading the LLMs"""

from langchain_ollama import ChatOllama


def initialize_llm():
    """Initialize the llm"""
    llm = ChatOllama(model="llama3.2:3b", temperature=0.5)
    return llm
