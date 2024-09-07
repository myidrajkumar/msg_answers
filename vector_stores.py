"""Vector Stores"""

from langchain_core.chat_history import InMemoryChatMessageHistory
from prompt_message_formats import get_system_prompt

store = {}


def get_session_history(session_id: str):
    """Get the session history"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory(encode="UTF-8")
    return store[session_id]


def build_system_prompt(question, collection):
    """Construct System Prompt"""
    results = collection.query(
        query_texts=[question],
        n_results=1,
    )
    return get_system_prompt(results)
