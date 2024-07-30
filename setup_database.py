import os

from langchain_community.embeddings import OpenAIEmbeddings
#from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def create_chroma_db(file_path):
    """Creates a ChromaDB database and populates it with embeddings from a text file.

    Args:
        file_path: Path to the text file.
    """

    loader = TextLoader(file_path)
    documents = loader.load()

    embeddings = OpenAIEmbeddings()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    docs = text_splitter.split_documents(documents)
    chroma_db1 = Chroma.from_documents(documents=docs,collection_name='vector_db1',
                embedding=embeddings, collection_metadata={"hnsw:space": "cosine"}, persist_directory="db1")
    chroma_db1.persist()


    vectorstore = Chroma.from_documents(documents, embeddings)

    # Persist the vectorstore to disk
    vectorstore.persist()

# Example usage
file_path = "transcribed_text1.txt"
create_chroma_db(file_path)
