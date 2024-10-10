"""Main Application"""

import uuid
from typing import Optional
import asyncio
import pyttsx3

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from answers_handling import answer_questions
from chromadb_load import load_documents_if_not_present, load_specific_doc
from send_mail import send_email
from vector_stores import get_session_history

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Main Page"""
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/token")
def get_token():
    """Retrieve Token"""
    session_id = str(uuid.uuid4())
    return {"token": session_id}


class QuestionRequest(BaseModel):
    """Request Parameters"""

    question: Optional[str] = None
    token: str
    department: str


@app.post("/ask")
async def ask(request: QuestionRequest):
    question = request.question
    session_id = request.token
    department = request.department

    async def generate():
        if department in ["Human Resources", "Finance", "IT"]:
            print(question, department, session_id)
            for chunk in answer_questions(question, department, session_id):
                if "answer" in chunk:
                    answer = chunk["answer"]
                    yield answer
                await asyncio.sleep(
                    0.05
                )  # Simulate delay(50 milliseconds) for smoother streaming
        else:
            print(question, department, session_id)
            yield "Invalid field selected."
        # speak_answer(answer)
        # threading.Thread(target=speak_answer, kwargs={"answer": answer}).start()

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/raiseconcernmail")
def raise_concern(request: QuestionRequest):
    """Sending concern"""
    try:
        department = request.department
        session_id = request.token
        sender = "admin@techinterrupt.com"
        if department == "Finance":
            receiver = "finance@techinterrupt.com"
            subject = "Finance Query"
        elif department == "Human Resources":
            receiver = "hr@techinterrupt.com"
            subject = "HR Query"
        elif department == "IT":
            receiver = "operations@techinterrupt.com"
            subject = "Operations Query"
        send_email(sender, receiver, subject, get_session_history(session_id))
        return {"success": True, "message": "Concern raised successfully"}

    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "message": "An error occurred"}, 500


@app.post("/fileupload")
def upload_file(department: str, file: UploadFile):
    """Uploading specific file"""

    # check if the post request has the file part
    if file.filename == "":
        return {"error": "No selected file"}, 400

    load_specific_doc(file, department)
    return {"message": "success"}, 200


def speak_answer(answer):
    """Speak the answer"""
    engine = pyttsx3.init()
    engine.say(answer)
    engine.runAndWait()


if __name__ == "__main__":
    load_documents_if_not_present()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
