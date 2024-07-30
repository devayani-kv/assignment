import os
import operator
import warnings
import json
import re

from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
#import google.generativeai as genai
#from langchain_chroma import Chroma
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List
from typing_extensions import TypedDict
from typing import List
from typing_extensions import TypedDict
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Ignore all warnings
warnings.filterwarnings("ignore")

chroma_db1 = Chroma(persist_directory="C:/Users/Devayani K/whisper/db1", embedding_function=OpenAIEmbeddings(),
                   collection_name='vector_db1')
similarity_threshold_retriever = chroma_db1.as_retriever(search_kwargs={"k": 3})
chatgpt = ChatOpenAI(model_name='gpt-4o', temperature=0)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def qa_rag_chain(query):

    '''This function essentially retrieves the answer from the RAG database
    Args: 
        query : query to extract the place that is being talked about in the transcribed text
        '''

    prompt = """You are an assistant for question-answering tasks.
                Use ONLY the following pieces of retrieved context to answer the question.
                Do not make up the answer unless it is there in the provided context.
                If the answer is not there in the provided context, ONLY say that you don't know the answer.
                Give a detailed answer and to the point answer with regard to the question.

                Question:
                {question}

                Context:
                {context}

                Answer:
            """
    prompt_template = ChatPromptTemplate.from_template(prompt)

    # create QA RAG chain
    qa_rag_chain = (
        {
            "context": (operator.itemgetter('context')
                            |
                        RunnableLambda(format_docs)),
            "question": operator.itemgetter('question')
        }
        |
        prompt_template
        |
        chatgpt
        |
        StrOutputParser()
    )

    top3_docs = similarity_threshold_retriever.get_relevant_documents(query)
    #print(top3_docs)
    result = qa_rag_chain.invoke(
        {"context": top3_docs, "question": query}
    )
    s = ''
    b = False
    for i in result:
        if i == '{':
            b = True
        if i == '}':
            s += i
            b = False
        if b == True:
            s += i
    return json.loads(s)

query = '''Can you pick out the names of any cities from the paragraph, not people from cities, only cities
            Return only the name of the city
            Return the answer as a json file with the key as the word "city" and the value as the extracted city'''
#ans = qa_rag_chain(query)

#print(ans)
#with open('country.json','w') as f:
    #data = json.loads(s)
    #json.dump(data, f)

