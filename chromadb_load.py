"""Loaded Chroma DB"""

import os
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
from werkzeug.utils import secure_filename

warnings.filterwarnings("ignore", category=FutureWarning)

HR_DEPARTMENT = "hr_department"
IT_DEPARTMENT = "it_department"
FINANCE_DEPARTMENT = "finance_department"

CHROMA_DB = "chromadb"
HR = "hr"
IT = "it"
FINANCE = "finance"

ROOT_DATA_DIR = r"data"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)


hr_db = Chroma(
    collection_name=HR_DEPARTMENT,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding_model,
    persist_directory="".join([CHROMA_DB, "/", HR]),
)
it_db = Chroma(
    collection_name=IT_DEPARTMENT,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding_model,
    persist_directory="".join([CHROMA_DB, "/", IT]),
)
finance_db = Chroma(
    collection_name=FINANCE_DEPARTMENT,
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding_model,
    persist_directory="".join([CHROMA_DB, "/", FINANCE]),
)


def check_if_docs_loaded(department_db):
    """Returns True if the database has documents, otherwise False"""
    return len(department_db.get()["documents"]) > 0


def get_loader_documents(file_path, category):
    """Get loader for documents"""

    documents = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for dir_path, _, files in os.walk(file_path):
        for available_file in files:
            file_name = os.path.join(dir_path, available_file)
            if available_file.endswith(".txt"):
                loader = TextLoader(file_name)
            elif available_file.endswith(".pdf"):
                loader = PyPDFLoader(file_name)
            elif available_file.endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(file_name)
            elif available_file.endswith(".pptx"):
                loader = UnstructuredPowerPointLoader(file_name)
            else:
                print(f"Unsupported file type for {file_name}")
                continue
            document = loader.load()
            for doc in document:
                doc.metadata["category"] = category
                doc.metadata["version"] = "v1"
                doc.metadata["upload_date"] = current_time
            documents.extend(document)

    return documents


def load_hr_document_if_not_present():
    """Loading HR documents if not added"""
    if check_if_docs_loaded(hr_db):
        print("HR documents already loaded")
        return

    directory = os.path.join(ROOT_DATA_DIR, HR)
    documents = get_loader_documents(directory, HR.upper())
    hr_db.add_texts([doc.page_content for doc in documents])
    print("HR documents now loaded")


def load_it_document_if_not_present():
    """Loading IT documents"""
    if check_if_docs_loaded(it_db):
        print("IT documents already loaded")
        return

    directory = os.path.join(ROOT_DATA_DIR, IT)
    documents = get_loader_documents(directory, IT.upper())
    it_db.add_texts([doc.page_content for doc in documents])
    print("IT documents now loaded")


def load_finance_document_if_not_present():
    """Loading Finance documents"""
    if check_if_docs_loaded(finance_db):
        print("Finance documents already loaded")
        return

    directory = os.path.join(ROOT_DATA_DIR, FINANCE)
    documents = get_loader_documents(directory, FINANCE.upper())
    finance_db.add_texts([doc.page_content for doc in documents])
    print("Finanace documents now loaded")


def load_documents_if_not_present():
    """Load all the available docs"""
    load_hr_document_if_not_present()
    load_it_document_if_not_present()
    load_finance_document_if_not_present()


def load_into_chromadb(file_content, db_name):
    """Loading specific document"""
    documents = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    filename = secure_filename(file_content.filename)
    if filename.endswith(".txt"):
        loader = TextLoader(file_content)
    elif filename.endswith(".pdf"):
        loader = PyPDFLoader(file_content)
    elif filename.endswith(".docx"):
        loader = UnstructuredWordDocumentLoader(file_content)
    elif filename.endswith(".pptx"):
        loader = UnstructuredPowerPointLoader(file_content)
    else:
        print(f"Unsupported file type for {filename}")

    document = loader.load()
    for doc in document:
        doc.metadata["upload_date"] = current_time
    documents.extend(document)

    db_name.add_texts([doc.page_content for doc in documents])


def load_specific_doc(doc_file, category):
    """Load specific doc"""

    filename = secure_filename(doc_file.filename)
    department_folder = get_folder_name(category)

    filename = "".join([department_folder, "/", filename])
    doc_file.save(filename)

    db_name = get_db(category)
    documents = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    document = loader.load()
    for doc in document:
        doc.metadata["upload_date"] = current_time
    documents.extend(document)

    db_name.add_texts([doc.page_content for doc in documents])
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
