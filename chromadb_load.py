import os

import chromadb
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_PATH = r"chroma_db"
ROOT_DIR = r"data"


for subdir, dirs, files in os.walk(ROOT_DIR):
    for directory in dirs:
        sub_directory = os.path.join(subdir, directory)
        collection_name = directory.lower()
        # print("Collection Name", collection_name)

        chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

        collection = chroma_client.get_or_create_collection(name=collection_name)

        loader = PyPDFDirectoryLoader(sub_directory)
        raw_documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_documents(raw_documents)

        documents = []
        metadata = []
        ids = []

        i = 0

        for chunk in chunks:
            documents.append(chunk.page_content)
            ids.append("ID" + str(i))
            metadata.append(chunk.metadata)

            i += 1

        collection.upsert(documents=documents, metadatas=metadata, ids=ids)
