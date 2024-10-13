"""Answer the questions"""

from chromadb_load import get_db
from vector_stores import get_retrieval_chain_for_db


async def get_stream_response(chat_rag_chain, session_id, question):
    """Getting Streamed Response"""

    for chunk in chat_rag_chain.stream(
        {"input": question},
        config={"configurable": {"session_id": session_id}},
    ):
        if chunk.get("answer"):
            yield chunk.get("answer")


def answer_questions(question, department, session_id):
    """Answer the questions"""

    department_db = get_db(department)
    conversational_rag_chain = get_retrieval_chain_for_db(department_db)
    return get_stream_response(conversational_rag_chain, session_id, question)
