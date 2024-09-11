import chromadb

from send_mail import send_email
from vector_stores import build_system_prompt, get_session_history
from lllms_handling import get_llm_answer, initialize_llm

from questions_handling import get_question, is_raise_concern


CHROMA_PATH = r"chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

llm = initialize_llm()

def answer_questions(session_id, question, department):

    collection = chroma_client.get_collection(name=department.lower().replace(' ', ''))

    while question:
        sys_prompt = build_system_prompt(question, collection)
        information = get_llm_answer(
            llm, sys_prompt, question, session_id)

        return information
