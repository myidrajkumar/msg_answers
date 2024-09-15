"""Main Application"""

import threading
import uuid

import pyttsx3
from flask import Flask, jsonify, render_template, request

from answers_handling import answer_questions
from chromadb_load import load_documents_if_not_present
from send_mail import send_email
from vector_stores import get_session_history, store_session_history

app = Flask(__name__)


@app.route("/")
def index():
    """Main Page"""
    return render_template("index.html")


@app.route("/token", methods=["GET"])
def get_token():
    """Retrieve Token"""
    session_id = str(uuid.uuid4())
    return jsonify({"token": session_id})


@app.route("/ask", methods=["POST"])
def ask():
    """Asking the question"""
    data = request.json
    field = data.get("field")
    question = data.get("question")
    session_id = data.get("token")
    department = data.get("department")

    if field in ["1", "2", "3"]:
        answer = answer_questions(question, department, session_id)
        store_session_history(session_id, question, answer)
    else:
        answer = "Invalid field selected."

    # speak_answer(answer)
    threading.Thread(target=speak_answer, kwargs={"answer": answer}).start()

    return jsonify({"content": answer})


@app.route("/raiseconcernmail", methods=["POST"])
def raise_concern():
    """Sending concern"""
    try:
        data = request.json
        department = data.get("department")
        session_id = data.get("token")
        sender = "admin@techinterrupt.com"
        if department == "Finance":
            receiver = "finance@techinterrupt.com"
            subject = "Finance Query"
        elif department == "Human Resources":
            receiver = "hr@techinterrupt.com"
            subject = "HR Query"
        elif department == "Operations":
            receiver = "operations@techinterrupt.com"
            subject = "Operations Query"
        send_email(sender, receiver, subject, get_session_history(session_id))
        return jsonify({"success": True, "message": "Concern raised successfully"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "An error occurred"}), 500


def speak_answer(answer):
    """Speak the answer"""
    engine = pyttsx3.init()
    engine.say(answer)
    engine.runAndWait()


if __name__ == "__main__":
    load_documents_if_not_present()
    app.run(debug=True)
