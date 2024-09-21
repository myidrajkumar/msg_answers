"""Prompt Formats"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_contextual_system_prompt():
    """Ask the system prompt"""
    return """
You need to answer the questions based on the below provided context.
 
Following are the guidelines
 
1. Use friendly tone only
2. Just answer the questions based on provided context
3. Do not use external knowledge to get the answer
4. Do not provide the answers in Markdown or md format
5. Instead of returning answers in Markdown, please return them in HTML format directly
6. Please provide the answers in HTML format ONLY
7. Add appropritate HTML tags like ul,li,a etc whereever needed
8. If the answer contains link, provide corresponding anchor tags
9. If the answer contains anchor tag, please add 'target' attribute as '_blank'
10. Do not use 'According to the context/text or Based on the context/text' in the answers
11. If the contenxt does not contain any relevant information to the question,
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
