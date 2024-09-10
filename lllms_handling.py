"""Loading the LLMs"""

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama
import json

from vector_stores import get_session_history


def initialize_llm():
    """Initialize the llm"""
    llm = ChatOllama(
        model="llama3.1:latest",
    )
    return llm


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

    response = with_message_history.invoke(
        {"messages": [HumanMessage(content=question)]},
        config={"configurable": {"session_id": session_id}},
    )
    content_data = {'content': response.content}
    content_json = json.dumps(content_data)
    return content_json

    # return "Requested question is out of my knowledge" in response.content
