"""ChatBot"""

import datetime
import uuid
import warnings

import chromadb
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

from finanace_answers import answer_finance_questions
from send_mail import send_email


warnings.filterwarnings("ignore")


print("\tWelcome to MSG!!!!")
print("We will answer all your questions")


def display_questions():
    """Displaying Questions"""
    print("\t1. Human Resources")
    print("\t2. Operations")
    print("\t3. Finance")
    print("\t4. Quit")

    return input("\nPlease choose your field: ")


def initialize_llm():
    """Initialize the llm"""
    llm = ChatOllama(
        model="llama3.1:latest",
    )
    return llm


def get_question():
    """Ask the question"""
    user_query = input("\nQuestion: ")
    return user_query


def get_system_prompt(results, team):
    """Ask the system prompt"""
    return (
        f"""
You must answer only based on the data given below.
Do NOT use your internal knowledge and do NOT share any other information.
When you are providing answer, no mention of 'text is provided' as such.
Just provide the answer from the below.
If you don't know the answer,
just say: As requested question is out of my knowledge,
Please consult {team}
--------------------
The data:
"""
        + str(results["documents"])
        + """
"""
    )


def is_raise_concern(field):
    """Getting concern"""
    print(
        f"""
As there is no data available, we could send your question to {field} team.
With this, your entire conversation history will be shared.
Also, as conversation submitted, this chat session will be closed.
"""
    )
    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Do you want to raise concern (1. Yes, 2. No): ")
    return choice == "1"


def get_llm_answer(llm, system_prompt, question, session_id, field):
    """Get the answer"""

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = prompt | llm

    with_message_history = RunnableWithMessageHistory(
        chain, get_session_history, input_messages_key="messages"
    )
    print(f"{field}: ", end="")

    response = with_message_history.invoke(
        {"messages": [HumanMessage(content=question)]},
        config={"configurable": {"session_id": session_id}},
    )
    print(response.content, flush=True)
    print()

    return "out of my knowledge" in response.content


def is_exit_field(question):
    """Need to be exited or not"""
    question = get_question()
    if question == "q":
        print("Bye!!!")
        return True
    return False


def build_system_prompt(question, team, collection):
    """Construct System Prompt"""
    results = collection.query(
        query_texts=[question],
        n_results=1,
    )
    return get_system_prompt(results, team)


def send_email_and_notify(sender, reciver, subject, message, field):
    """Send Mail and end the chat"""
    send_email(
        sender,
        reciver,
        subject,
        message,
    )
    print(f"Mail has been sent to {field} team. Thank you.\n\n")
    print("New chat session has been initiated")


def answer_operations_questions(session_id, field):
    """Answer operations"""
    llm = initialize_llm()
    collection = chroma_client.get_or_create_collection(name="operations")
    question = ""
    while question != "q":
        if is_exit_field(question):
            break

        results = collection.query(query_texts=[question], n_results=1)
        system_prompt = get_system_prompt(results, "Operations Team")
        is_no_information = get_llm_answer(
            llm, system_prompt, question, session_id, field
        )

        if is_no_information:
            is_send_mail = is_raise_concern(field)

            if not is_send_mail:
                continue

            send_email_and_notify(
                "admin@techinterrupt.com",
                "operations@techinterrupt.com",
                "Operations Query",
                "Hello",
                field,
            )
            break


def answer_humanresources_questions(session_id, field):
    """Answer human resources questions"""
    llm = initialize_llm()
    collection = chroma_client.get_or_create_collection(name="humanresources")

    question = ""
    while question != "q":
        if is_exit_field(question):
            break

        results = collection.query(query_texts=[question], n_results=1)
        system_prompt = get_system_prompt(results, "HR Team")
        is_no_information = get_llm_answer(
            llm, system_prompt, question, session_id, field
        )

        if is_no_information:
            is_send_mail = is_raise_concern(field)

            if not is_send_mail:
                continue

            send_email_and_notify(
                "admin@techinterrupt.com",
                "hr@techinterrupt.com",
                "HR Query",
                "Hello",
                field,
            )
            break


store = {}


def get_session_history(session_id: str):
    """Get the session history"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


CHROMA_PATH = r"chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

sessionid = uuid.uuid4()
choosen_field = ""
while choosen_field != "4":
    choosen_field = display_questions()
    if choosen_field == "1":
        answer_humanresources_questions(sessionid, "HR")
    elif choosen_field == "2":
        answer_operations_questions(sessionid, "IT")
    elif choosen_field == "3":
        answer_finance_questions(sessionid)
    elif choosen_field == "4":
        hour = datetime.datetime.now().hour
        greeting = "Have a nice day!" if hour < 20 else "Good night!"
        print("I look forward to our next meeting!", greeting)
    else:
        print("Invalid choice. Please choose either 1 or 2 or 3 or 4 only. \n")
