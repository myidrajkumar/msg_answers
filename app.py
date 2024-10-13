"""Main Application"""

import uuid
from typing import Optional


from fastapi import FastAPI, Request, Response, UploadFile, status
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from answers_handling import answer_questions
from chromadb_load import (
    delete_doc,
    get_all_db_docs,
    get_db_docs,
    load_documents_if_not_present,
    load_specific_doc,
    update_doc,
)
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
    """Asking the question"""
    question = request.question
    session_id = request.token
    department = request.department

    if department in ["Human Resources", "Finance", "IT"]:
        print(question, department, session_id)
        answer = answer_questions(question, department, session_id)
    else:
        print(question, department, session_id)
        answer = "Invalid field selected."

    return StreamingResponse(answer, media_type="text/event-stream")


@app.post("/raiseconcernmail", status_code=status.HTTP_200_OK)
def raise_concern(request: QuestionRequest, response: Response):
    """Sending concern"""
    try:
        department = request.department
        session_id = request.token
        sender = "admin@techinterrupt.com"
        receiver = None
        subject = None
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
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "message": "An error occurred"}


class FileRequestPayload(BaseModel):
    """File Request Model"""

    department: str
    version: str
    tags: str


@app.post("/fileupload")
def upload_file(file: UploadFile, department: str, version: str, tags: str):
    """Uploading specific file"""

    # check if the post request has the file part
    if file.filename == "":
        return {"error": "No selected file"}, 400

    payload = FileRequestPayload(department=department, version=version, tags=tags)
    load_specific_doc(file, payload)
    return {"message": "success"}


@app.get("/list", status_code=status.HTTP_200_OK)
def get_docs_list(department: Optional[str] = None):
    """Getting docs list"""

    if department is None:
        docs = get_all_db_docs()
    else:
        docs = get_db_docs(department)

    return {"data": docs, "message": "Success"}


@app.post("/fileupdate")
def update_file(file: UploadFile, department: str, version: str, tags: str):
    """Uploading specific file"""

    # check if the post request has the file part
    if file.filename == "":
        return {"error": "No selected file"}, 400

    payload = FileRequestPayload(department=department, version=version, tags=tags)
    update_doc(file, payload)
    return {"message": "success"}


@app.get("/filedelete")
def delete_file(department: str, filename: str):
    """Deleting specific file"""

    delete_doc(department, filename)
    return {"message": "success"}


if __name__ == "__main__":
    load_documents_if_not_present()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
