"""Prompt Formats"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_contextual_system_prompt():
    """Ask the system prompt"""
    return """
You are an assistant for question-answering tasks.Use the following pieces of retrieved context to answer.

Following are the guidelines for answering the questions:

1. Use friendly tone only
2. Just answer the questions based on provided context
3. Do not use external knowledge to get the answer
4. DO NOT PROVIDE THE ANSWERS IN MARKDOWN OR MD FORMAT AT ALL
5. Convert the answer to HTML if MARKDOWN format is present
6. Please provide the answers in HTML format ONLY ALWAYS
7. Add appropritate HTML tags like ul,li,a etc whereever needed
8. If the answer contains link, provide corresponding anchor tags
9. If the answer contains anchor tag, please add 'target' attribute as '_blank'
11. If the context does not contain any relevant information to the question,
   then, DO NOT make something up and just say 'This is out of my knowledge'

<context>
{context}
</context>
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
