"""Prompt Formats"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_contextual_system_prompt():
    """Ask the system prompt"""
    return """
You are an assistant for question-answering tasks.
Use the retrieved context ONLY to answer the question.
If you don't know the answer, just say that 'This is out of my knowledge'

Context: {context}

Following are the guidelines for answering the questions:

1. Use friendly tone only
2. Just answer the questions based on the retrieved context
3. Do not use your knowledge to get the answer
4. Please provide the answers in HTML format ONLY ALWAYS
5. The Font color of HTML should be 'black'
6. DO NOT PROVIDE THE ANSWERS IN MARKDOWN OR MD FORMAT AT ALL
7. Convert the answer to HTML even if MARKDOWN format is present
8. Add appropritate HTML tags like ul,li,a etc whereever needed
9. If the answer contains link, provide corresponding anchor tags
10. If the answer contains anchor tag, please add 'target' attribute as '_blank'
11. If the context does not contain any relevant information to the question,
   then, DO NOT make something up and just say 'This is out of my knowledge'

YOU CANNOT PROVIDE A ANSWER IF IT DOES NOT APPEAR IN RETRIEVED CONTEXT AND JUST SAY 'This is out of my knowledge'.   
            """


def get_question_prompt():
    """The prompt for questions"""
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                get_contextual_system_prompt(),
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )


def get_retriever_prompt():
    """The prompt for Chroma DB"""
    retriever_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            (
                "human",
                "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation",
            ),
        ]
    )

    return retriever_prompt
