"""To handle the questions"""


def get_question(question):
    """Need to be exited or not"""
    question = get_input_question()
    if question == "q":
        print("Bye!!!")
        return None
    return question


def get_input_question():
    """Ask the question"""
    user_query = input("\nQuestion: ")
    return user_query


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
