"""Vector Stores"""

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from lllms_handling import initialize_llm
from prompt_message_formats import get_history_contextual_prompt, get_question_prompt

store = {}
user_conversations = {}

llm = initialize_llm()


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get the conversation history"""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def store_session_history(session_id: str, question: str, answer: str):
    """Store the session history"""
    conversation_history = user_conversations.get(session_id, [])
    conversation_history.append(HumanMessage(content=question))
    conversation_history.append(AIMessage(content=answer))
    user_conversations[session_id] = conversation_history


def get_retrieval_chain_for_db(department_db: Chroma):
    """Get the retrieval chain"""

    retriever = department_db.as_retriever(search__kwargs={"k": 1})

    contextualize_history_prompt = get_history_contextual_prompt()
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_history_prompt
    )

    # Answer question
    qa_prompt = get_question_prompt()
    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return conversational_rag_chain
