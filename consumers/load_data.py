
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import FAISS
import constants
import os

from langchain.document_loaders import PyPDFLoader
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = constants.MODEL_SECRET_FILEPATH


def load_data():
    print("Starting: " + os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

    loader = PyPDFLoader(constants.MODEL_DATA_PATH + '/EventData.pdf')

    # split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=constants.MODEL_BATCH_CHUNK_SIZE, chunk_overlap=constants.MODEL_CHUNK_OVERLAP)
    pages = loader.load_and_split(text_splitter=text_splitter)

    embeddings = VertexAIEmbeddings()

    # Use Langchain to create the embeddings using text-embedding-ada-002
    db = FAISS.from_documents(documents=pages, embedding=embeddings)

    # save the embeddings into FAISS vector store
    db.save_local(folder_path=constants.MODEL_DB_SAVE_PATH,
                  index_name=constants.MODEL_DB_INDEX_NAME)

    # embeddings = VertexAIEmbeddings()
    # ###### SAVE DATA #############
    # loader = DirectoryLoader(constants.MODEL_DATA_PATH)
    # documents = loader.load()
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=constants.MODEL_BATCH_CHUNK_SIZE, chunk_overlap=constants.MODEL_CHUNK_OVERLAP)
    # docs = text_splitter.split_documents(documents)
    # knowledge_base = FAISS.from_documents(docs, embeddings)
    # knowledge_base.save_local(folder_path=constants.MODEL_DB_SAVE_PATH,
    #                           index_name=constants.MODEL_DB_INDEX_NAME)
    print("ended")


if __name__ == "__main__":
    load_data()
