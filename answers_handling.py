"""Answer the questions"""

from chromadb_load import get_db
from vector_stores import get_retrieval_chain_for_db, get_session_history


def answer_questions(question, department, session_id):
    """Answer the questions"""

    conversation_history = get_session_history(session_id)
    department_db = get_db(department)
    retrieval_chain = get_retrieval_chain_for_db(department_db)

    response = retrieval_chain.invoke(
        {"input": question, "chat_history": conversation_history}
    )

    return response["answer"]
