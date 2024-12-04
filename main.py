# import os
# import streamlit as st
# import pickle
# import time
# from langchain.chains import RetrievalQAWithSourcesChain
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain_openai import OpenAIEmbeddings, OpenAI
# from langchain_community.vectorstores import FAISS
# from dotenv import load_dotenv

# load_dotenv()  # extracts environment variables from .env file -api key loaded

# key = "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"

# # App Title and Description
# st.set_page_config(page_title="News Research Tool", layout="wide")
# st.title("📰 FinSight: Your Financial Research Assistant")
# st.markdown("""
#     Welcome to the **News Research Tool**! This application is designed for financial research analysts to retrieve insights quickly from multiple articles using AI-powered search. 
#     Simply enter the URLs of the news articles and ask your query below.
# """)

# # Sidebar for URLs Input
# st.sidebar.title("🔗 News Article URLs")
# st.sidebar.info("Enter up to 5 article URLs for processing:")
# urls = []
# for i in range(5):
#     url = st.sidebar.text_input(f"URL {i+1}")
#     urls.append(url)

# process_url_button_clicked = st.sidebar.button("🚀 Process URLs")

# # Set pickle file name that will be later stored on disk
# file_path = "faiss_store_openai.pkl"

# # Let's create a status tracker
# main_placefolder = st.empty()

# # Create LLM object for later use
# llm = OpenAI(temperature=0.9, max_tokens=500)

# # Process URLs and create vector store
# if process_url_button_clicked:
#     if any(urls):  # Ensure at least one URL is provided
#         # Load the data
#         loader = UnstructuredURLLoader(urls=urls)
#         main_placefolder.text("🔄 Data Loading Started...")
#         data = loader.load()

#         # Split the data
#         text_splitter = RecursiveCharacterTextSplitter(
#             separators=["\n", ".", " "],
#             chunk_size=500,    # size of each block of data
#             chunk_overlap=100  # how many tokens from previous block be included in subsequent chunks
#         )
#         main_placefolder.text("🔄 Data loaded successfully. Splitting data into chunks...")
#         docs = text_splitter.split_documents(data)

#         # Create embeddings and save to FAISS index
#         embeddings = OpenAIEmbeddings(api_key=key)
#         vectorstore_openai = FAISS.from_documents(docs, embeddings)
#         main_placefolder.text("🔄 Data split successfully. Creating embedding vectors...")
#         time.sleep(2)

#         # Save FAISS index to disk
#         file_path = "faiss_index"
#         vectorstore_openai.save_local(file_path)  # Save in-memory FAISS index to disk
#         main_placefolder.success("✅ Vectors created and saved successfully.")
#     else:
#         st.sidebar.error("Please provide at least one valid URL.")

# # User Input for Query
# st.subheader("🔍 Ask Your Query")
# query = st.text_input("How can I help you?", placeholder="Type your financial query here...")

# # Answer Retrieval and Display
# if query:
#     if os.path.exists(file_path):  # check if our vector file path exists -> URLs processed earlier
#         vectorstore = FAISS.load_local(file_path, embeddings,
#                                        allow_dangerous_deserialization=True)  # Load the FAISS index

#         chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())

#         result = chain.invoke({"question": query}, return_only_outputs=True)

#         # Display the Answer
#         st.header("📋 Answer")
#         st.markdown(result["answer"], unsafe_allow_html=True)

#         # Display Sources
#         sources = result.get("sources", "")
#         if sources:
#             st.subheader("📚 Sources")
#             sources_lst = sources.split("\n")
#             for source in sources_lst:
#                 st.markdown(f"- {source}")
#     else:
#         st.error("❌ No processed data found. Please process URLs first.")


# # Footer
# st.markdown("""
#     ---
#     🔗 Created with ❤️ by Feroz Khan for financial research analysts.
# """)


import os
import streamlit as st
import time
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()  # extracts environment variables from .env file - API key loaded

key = "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"

# App Title and Description
st.set_page_config(page_title="News Research Tool", layout="wide")
st.title("📰 FinSight: Your Financial Research Assistant")

# Sidebar for URLs Input
st.sidebar.title("🔗 News Article URLs")
st.sidebar.info("Enter up to 5 article URLs for processing:")
urls = []
for i in range(5):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_button_clicked = st.sidebar.button("🚀 Process URLs")

# Session state to store FAISS vectorstore
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None  # Initialize vectorstore as None

# LLM Setup
llm = OpenAI(temperature=0.9, max_tokens=500)

# Process URLs and create vectorstore
if process_url_button_clicked:
    if any(urls):  # Ensure at least one URL is provided
        # Load the data
        loader = UnstructuredURLLoader(urls=urls)
        st.info("🔄 Data Loading Started...")
        data = loader.load()

        # Split the data
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n", ".", " "],
            chunk_size=500,    # size of each block of data
            chunk_overlap=100  # how many tokens from previous block be included in subsequent chunks
        )
        st.info("🔄 Data loaded successfully. Splitting data into chunks...")
        docs = text_splitter.split_documents(data)

        # Create embeddings and FAISS index
        embeddings = OpenAIEmbeddings(api_key=key)
        vectorstore_openai = FAISS.from_documents(docs, embeddings)

        # Save FAISS index to disk and session state
        file_path = "faiss_index"
        vectorstore_openai.save_local(file_path)  # Save FAISS index
        st.session_state.vectorstore = vectorstore_openai  # Persist vectorstore in session

        st.success("✅ Vectors created and saved successfully.")
    else:
        st.sidebar.error("Please provide at least one valid URL.")

# User Input for Query
st.subheader("🔍 Ask Your Query")
query = st.text_input("How can I help you?", placeholder="Type your financial query here...")

# Answer Retrieval and Display
if query:
    if st.session_state.vectorstore:  # Check if vectorstore exists in session state
        vectorstore = st.session_state.vectorstore

        # Create retrieval chain
        chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
        result = chain({"question": query}, return_only_outputs=True)

        # Display the Answer
        st.header("📋 Answer")
        st.markdown(result["answer"], unsafe_allow_html=True)

        # Display Sources
        sources = result.get("sources", "")
        if sources:
            st.subheader("📚 Sources")
            sources_lst = sources.split("\n")
            for source in sources_lst:
                st.markdown(f"- {source}")
    else:
        st.error("❌ No processed data found. Please process URLs first.")

# Footer
st.markdown("""
    ---
    🔗 Made with ❤️ by Feroz Khan for financial research analysts.
""")
