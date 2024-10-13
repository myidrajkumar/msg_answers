"""Answer the questions"""

from chromadb_load import get_db
from vector_stores import get_retrieval_chain_for_db


def answer_questions(question, department, session_id):
    """Answer the questions"""

    department_db = get_db(department)
    conversational_rag_chain = get_retrieval_chain_for_db(department_db)

    return conversational_rag_chain.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}},
    )["answer"]
