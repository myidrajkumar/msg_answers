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
6. Add appropritate HTML tags like ul,li,a etc whereever needed
7. If the answer contains link to external site, provide corresponding anchor tags
8. If the answer contains anchor tag, please add 'target' attribute as '_blank'
9. DO NOT PROVIDE THE ANSWERS IN MARKDOWN OR MD FORMAT AT ALL
10. Convert the answer to HTML even if MARKDOWN format is present
11. If the context does not contain any relevant information to the question,
   then, DO NOT make something up and just say 'This is out of my knowledge'

Constraints:
1. DO NOT PROVIDE ANY EXPLANATION OR DETAILS OR MENTION THAT YOU WERE GIVEN CONTEXT.
2. Don't mention that you are not able to find the answer in the provided context.
3. Don't make up the answers by yourself.
4. Try your best to provide answer from the retrieved context.

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


def get_history_contextual_prompt():
    """Getting Chat History prompt"""

    # Contextualize question
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
