"""Only answers HR Questions"""

import chromadb

from send_mail import send_email
from vector_stores import build_system_prompt, get_session_history
from lllms_handling import get_llm_answer, initialize_llm

from questions_handling import get_question, is_raise_concern


CHROMA_PATH = r"chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

DEPARTMENT = "Human Resources"

llm = initialize_llm()


def send_email_and_notify(sender, reciver, subject, message):
    """Send Mail and end the chat"""
    send_email(
        sender,
        reciver,
        subject,
        message,
    )
    print(f"Mail has been sent to {DEPARTMENT} team. Thank you.\n\n")
    print("New chat session has been initiated")


def answer_hr_questions(session_id):
    """Answer questions from the HR"""

    collection = chroma_client.get_collection(name="humanresources")

    question = ""
    while question != "q":
        question = get_question(question)
        if question is None:
            break

        sys_prompt = build_system_prompt(question, collection)
        is_no_information = get_llm_answer(
            llm, sys_prompt, question, session_id, DEPARTMENT
        )

        if is_no_information:
            is_send_mail = is_raise_concern(DEPARTMENT)
            if not is_send_mail:
                continue

            send_email_and_notify(
                "admin@techinterrupt.com",
                "hr@techinterrupt.com",
                "HR Query",
                get_session_history(session_id),
            )
            break