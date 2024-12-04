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

key = "Removed key for safety purpose"

# App Title and Description
st.set_page_config(page_title="News Research Tool", layout="wide")
st.title("📰 FinSight: Your Financial Research Assistant")

# I am adding a Sidebar for URLs Input
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
