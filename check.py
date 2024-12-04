import os
import streamlit as st
import pickle
import time
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_openai import OpenAIEmbeddings, OpenAI

from langchain_community.vectorstores import FAISS



from dotenv import load_dotenv
load_dotenv()  #extracts environment variables from .env file -api key loaded

key = "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"

st.title("News Research Tool")

st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)
process_url_button_clicked = st.sidebar.button("Process URLs")

#Set pickle file name that will be later stored on disk
file_path = "faiss_store_openai.pkl"

#Let's create a status tracker 
main_placefolder = st.empty()

#Create LLM object for later use
llm = OpenAI(temperature=0.9, max_tokens=500)

if process_url_button_clicked:
    
    #Load the data
    loader = UnstructuredURLLoader(urls = urls)
    main_placefolder.text("Data Loading Started...")
    data = loader.load()

    #Split the data
    text_splitter = RecursiveCharacterTextSplitter(
        separators= ["\n","."," "],
        chunk_size = 500,    #size of each block of data
        chunk_overlap = 100  #how many tokens from previous block be included in subsequent chunks
    )
    main_placefolder.text("Data loaded Successfully. Data Splitting Started...")
    
    docs = text_splitter.split_documents(data)
   
    #Create embeddings and save to FAISS index
    embeddings = OpenAIEmbeddings(api_key=key)
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    main_placefolder.text("Data splitted Successfully. Creating embedding vectors now...")
    time.sleep(2)

    file_path = "faiss_index"

    vectorstore_openai.save_local(file_path)  # Save in-memory FAISS index to disk

    main_placefolder.text("Vectors created and saved successfully.")
    time.sleep(2)



#Taking user question as input
query = main_placefolder.text_input("How can I help you?")

if query:
    if os.path.exists(file_path):    #check if our vector file path exists -> URLs processed earlier
        vectorstore = FAISS.load_local(file_path, embeddings,
                              allow_dangerous_deserialization=True)  # Load the FAISS index
        
        chain = RetrievalQAWithSourcesChain.from_llm(llm = llm, retriever = vectorstore.as_retriever())

        result =chain({"question": query}, return_only_outputs=True)
        # {"answer": "", "sources": []}

        st.header("Sure, here is what I could find:")
        st.subheader(result["answer"])

        #Let's also display source of information displayed 
        sources = result.get("sources","")
        if sources:
            st.subheader("Sources:")
            sources_lst = sources.split("\n")
            for source in sources_lst:
                st.write(source)
