"""ChatBot"""

import datetime
import uuid
import warnings


from finanace_answers import answer_finance_questions
from hr_answers import answer_hr_questions
from operation_answers import answer_operation_questions


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


sessionid = uuid.uuid4()
choosen_field = ""
while choosen_field != "4":
    choosen_field = display_questions()
    if choosen_field == "1":
        answer_hr_questions(sessionid)
    elif choosen_field == "2":
        answer_operation_questions(sessionid)
    elif choosen_field == "3":
        answer_finance_questions(sessionid)
    elif choosen_field == "4":
        hour = datetime.datetime.now().hour
        greeting = "Have a nice day!" if hour < 20 else "Good night!"
        print("I look forward to our next meeting!", greeting)
    else:
        print("Invalid choice. Please choose either 1 or 2 or 3 or 4 only. \n")
