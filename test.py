import os
import streamlit as st
import pickle
import time
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.vectorstores import FAISS
from langchain_community.document_loaders import UnstructuredURLLoader


loader = UnstructuredURLLoader(url = "https://www.yahoo.com/news/man-went-missing-1999-found-192000332.html")
data = loader.load()

print(data)

print("Sucess Loading")

text_splitter = RecursiveCharacterTextSplitter(
        separators= ["\n","."," "],
        chunk_size = 500,
        chunk_overlap = 100
    )

docs = text_splitter.split_documents(data)

print(docs[0])

print("Success Splitting")