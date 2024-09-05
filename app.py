from langchain_ollama import ChatOllama
import chromadb
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

import warnings

warnings.filterwarnings("ignore")


print("\tWelcome to MSG!!!!")
print("We will answer all your questions")
print("\t1. Human Resources")
print("\t2. Operations")
print("\t3. Finance")


def initialize_llm():
    """Initialize the llm"""
    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0.5,
    )
    return llm


def get_question():
    """Ask the question"""
    user_query = input("\nQuestion?\n\n")
    return user_query


def get_system_prompt(results, team):
    """Ask the system prompt"""
    return (
        f"""
    You are a helpful assistant.
    You are going to answer only based on the knowledge I'm providing to you. 
    You don't use your internal knowledge and you don't make thins up.
    If you don't know the answer, just say: Please consult {team}
    --------------------
    The data:
    """
        + str(results["documents"])
        + """
    """
    )


def get_llm_answer(llm, system_prompt, question, session_id):
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
    for r in with_message_history.stream(
        {"messages": [HumanMessage(content=question)]},
        config={"configurable": {"session_id": session_id}},
    ):
        print(r.content, end="", flush=True)
    print()


def answer_operations_questions(session_id):
    """Answer operations"""
    llm = initialize_llm()
    collection = chroma_client.get_or_create_collection(name="operations")
    question = ""
    while question != "q":
        question = get_question()
        if question == "q":
            print("Bye!!!")
            break
        else:
            results = collection.query(query_texts=[question], n_results=1)
            system_prompt = get_system_prompt(results, "Operations Team")
            get_llm_answer(llm, system_prompt, question, session_id)


def answer_humanresources_questions(session_id):
    """Answer human resources questions"""
    llm = initialize_llm()
    collection = chroma_client.get_or_create_collection(name="humanresources")
    question = ""
    while question != "q":
        question = get_question()
        if question == "q":
            print("Bye!!!")
            break
        else:
            results = collection.query(query_texts=[question], n_results=1)
            system_prompt = get_system_prompt(results, "HR Team")
            get_llm_answer(llm, system_prompt, question, session_id)


def answer_finance_questions(session_id):
    """Answer questions from the financial"""
    llm = initialize_llm()
    collection = chroma_client.get_or_create_collection(name="finance")
    question = ""
    while question != "q":
        question = get_question()
        if question == "q":
            print("Bye!!!")
            break
        else:
            results = collection.query(query_texts=[question], n_results=1)
            system_prompt = get_system_prompt(results, "Finance Team")
            get_llm_answer(llm, system_prompt, question, session_id)


store = {}


def get_session_history(session_id: str):
    """Get the session history"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


CHROMA_PATH = r"chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

sessionid = "abc123"
choice = input("Please choose your field: ")
if choice == "1":
    answer_humanresources_questions(sessionid)
elif choice == "2":
    answer_operations_questions(sessionid)
elif choice == "3":
    answer_finance_questions(sessionid)
