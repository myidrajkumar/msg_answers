"""Vector Stores"""

from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.messages import AIMessage, HumanMessage

from lllms_handling import initialize_llm
from prompt_message_formats import (
    get_question_prompt,
    get_retriever_prompt,
)

store = {}
user_conversations = {}

llm = initialize_llm()


def get_session_history(session_id: str):
    """Get the conversation history"""
    return user_conversations.get(session_id, [])


def store_session_history(session_id: str, question: str, answer: str):
    """Store the session history"""
    conversation_history = user_conversations.get(session_id, [])
    conversation_history.append(HumanMessage(content=question))
    conversation_history.append(AIMessage(content=answer))
    user_conversations[session_id] = conversation_history


def get_retrieval_chain_for_db(department_db):
    """Get the retrieval chain"""
    prompt = get_question_prompt()
    chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    retriever = department_db.as_retriever(search__kwargs={"k": 3})
    retriever_prompt = get_retriever_prompt()
    history_aware_retriever = create_history_aware_retriever(
        llm=llm, retriever=retriever, prompt=retriever_prompt
    )
    retrieval_chain = create_retrieval_chain(history_aware_retriever, chain)
    return retrieval_chain
