"""Answer the questions"""

from chromadb_load import finance_db, hr_db, it_db
from vector_stores import get_retrieval_chain_for_db, get_session_history


def answer_questions(question, department, session_id):
    """Answer the questions"""

    conversation_history = get_session_history(session_id)
    department_db = get_db_name(department)
    retrieval_chain = get_retrieval_chain_for_db(department_db)

    response = retrieval_chain.invoke(
        {"input": question, "chat_history": conversation_history}
    )

    return response["answer"]


def get_db_name(department):
    """Get Collection Name"""
    if department == "Human Resources":
        return hr_db
    elif department == "IT":
        return it_db
    elif department == "Finance":
        return finance_db
