"""Loaded Chroma DB"""

import os
import pathlib
import shutil
import warnings
from datetime import datetime

from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel

warnings.filterwarnings("ignore", category=FutureWarning)

HR_DEPARTMENT = "hr_department"
IT_DEPARTMENT = "it_department"
FINANCE_DEPARTMENT = "finance_department"

CHROMA_DB = "chromadb"
HR = "hr"
IT = "it"
FINANCE = "finance"

ROOT_DATA_DIR = r"data"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


hr_db = Chroma(
    collection_name=HR_DEPARTMENT,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embeddings,
    persist_directory="".join([CHROMA_DB, "/", HR]),
)
it_db = Chroma(
    collection_name=IT_DEPARTMENT,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embeddings,
    persist_directory="".join([CHROMA_DB, "/", IT]),
)
finance_db = Chroma(
    collection_name=FINANCE_DEPARTMENT,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embeddings,
    persist_directory="".join([CHROMA_DB, "/", FINANCE]),
)


def check_if_docs_loaded(department_db):
    """Returns True if the database has documents, otherwise False"""
    return len(department_db.get()["documents"]) > 0


def get_doc_file_loader(filename):
    """Get doc loader"""
    if filename.endswith(".txt"):
        loader = TextLoader(filename)
    elif filename.endswith(".pdf"):
        loader = PyPDFLoader(filename)
    elif filename.endswith(".docx"):
        loader = UnstructuredWordDocumentLoader(filename)
    elif filename.endswith(".pptx"):
        loader = UnstructuredPowerPointLoader(filename)
    else:
        print(f"Unsupported file type for {filename}")
        loader = None
    return loader


def add_metadata_to_doc(file_name, payload, loader):
    """Attaching Metadata"""

    documents = loader.load()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for doc in documents:
        doc.metadata["upload_date"] = current_time
        doc.metadata["title"] = file_name
        doc.metadata["version"] = payload.version
        doc.metadata["tags"] = payload.tags

    return documents


class Payload(BaseModel):
    """Request Parameters"""

    version: str
    tags: str


def split_text(documents_list):
    """Split the Document objects into smaller chunks."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    return text_splitter.split_documents(documents_list)


def get_doc_directory_loader(file_path, category):
    """Get loader for documents"""

    documents = []
    payload = Payload(version="1.0", tags=category)

    for dir_path, _, files in os.walk(file_path):
        for available_file in files:
            file_name = os.path.join(dir_path, available_file)
            loader = get_doc_file_loader(file_name)
            if loader is None:
                continue

            docs_with_meta = add_metadata_to_doc(available_file, payload, loader)
            chunks = split_text(docs_with_meta)
            documents.extend(chunks)

    return documents


def load_hr_document_if_not_present():
    """Loading HR documents if not added"""
    if check_if_docs_loaded(hr_db):
        print("HR documents already loaded")
        return

    directory = os.path.join(ROOT_DATA_DIR, HR)
    documents = get_doc_directory_loader(directory, HR.upper())
    hr_db.add_documents(documents)
    print("HR documents now loaded")


def load_it_document_if_not_present():
    """Loading IT documents"""
    if check_if_docs_loaded(it_db):
        print("IT documents already loaded")
        return

    directory = os.path.join(ROOT_DATA_DIR, IT)
    documents = get_doc_directory_loader(directory, IT.upper())
    it_db.add_documents(documents)
    print("IT documents now loaded")


def load_finance_document_if_not_present():
    """Loading Finance documents"""
    if check_if_docs_loaded(finance_db):
        print("Finance documents already loaded")
        return

    directory = os.path.join(ROOT_DATA_DIR, FINANCE)
    documents = get_doc_directory_loader(directory, FINANCE.upper())
    finance_db.add_documents(documents)
    print("Finanace documents now loaded")


def load_documents_if_not_present():
    """Load all the available docs"""
    load_hr_document_if_not_present()
    load_it_document_if_not_present()
    load_finance_document_if_not_present()


def save_department_doc(doc_file, payload):
    """Saving doc under department"""
    filename = doc_file.filename
    department_folder = get_folder_name(payload.department)

    filename = "".join([department_folder, "/", filename])
    pathlib.Path(filename).parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "wb+") as file_object:
        shutil.copyfileobj(doc_file.file, file_object)

    return filename


def load_specific_doc(doc_file, payload):
    """Load specific doc"""

    filename = save_department_doc(doc_file, payload)
    db_name = get_db(payload.department)

    loader = get_doc_file_loader(filename)
    if loader is None:
        return

    documents = add_metadata_to_doc(doc_file, payload, loader)
    chunks = split_text(documents)

    db_name.add_documents(chunks)

    print(f"{filename} document is now loaded")


def get_db_name(department):
    """Get Collection Name"""
    if department == "Human Resources":
        return HR_DEPARTMENT
    elif department == "IT":
        return IT_DEPARTMENT
    elif department == "Finance":
        return FINANCE_DEPARTMENT
    else:
        return None


def get_folder_name(department):
    """Get Folder Name"""
    if department == "Human Resources":
        return ROOT_DATA_DIR + "/" + HR
    elif department == "IT":
        return ROOT_DATA_DIR + "/" + IT
    elif department == "Finance":
        return ROOT_DATA_DIR + "/" + FINANCE
    else:
        return None


def get_db(department):
    """Get Collection"""
    if department == "Human Resources":
        return hr_db
    elif department == "IT":
        return it_db
    elif department == "Finance":
        return finance_db
    else:
        return None
