# **FinSight: Financial Research Assistant with LangChain and OpenAI**

## **Overview**  
FinSight is an AI-powered financial research assistant designed to streamline the workflow of research analysts. By leveraging LangChain, OpenAI's GPT models, and FAISS vector database, this tool provides quick and precise answers to complex financial queries based on data from news articles and financial reports.

---

## **Features**  
- Extracts and processes content from up to five URLs.  
- Splits and stores text in an optimized vector database using FAISS.  
- Enables semantic search for retrieving the most relevant text chunks.  
- Generates accurate answers via OpenAI's GPT model.  
- Cost-efficient by optimizing API token usage.

---

## **Technologies Used**  
- **Python**: Core programming language.  
- **LangChain**: For text chunking and query chains.  
- **OpenAI GPT**: For generating insightful answers.  
- **FAISS (Facebook AI Similarity Search)**: Vector database for fast, semantic search.  
- **Streamlit**: Interactive front-end interface.  

---

## **Getting Started**  

### **Prerequisites**  
Ensure you have the following installed:
- Python 3.8 or later  
- pip (Python package manager)  
- API key for OpenAI  

### **Installation**  
1. Clone this repository:
   ```bash
   git clone https://github.com/ferozk0333/FinSight-Financial-Research-Assistant-with-LangChain-and-OpenAI.git
   cd FinSight-Financial-Research-Assistant-with-LangChain-and-OpenAI
   ```
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up OpenAI API Key:
   Ideally, create a .env file in the project directory and add:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```
4. Run app:
   ```bash
   streamlit run main.py
   ```

---

## **Technical Architecture**  
### **Data Flow**
- **Document Loader**: Extracts article content and metadata from URLs.
- **Text Splitter**: Splits content into smaller, overlapping chunks using LangChain's RecursiveCharacterTextSplitter.
- **Vector Embedding**: Converts text chunks into embeddings via HuggingFace SentenceTransformers.
- **Vector Database**: Stores embeddings in FAISS for fast similarity search.
- **Query Processing**: Fetches relevant chunks and sends them to OpenAI for answering the user query.

---

## **UI & Flow Diagrams**
![ERA - UI_1](https://github.com/user-attachments/assets/6cd12ec4-1889-4747-9831-de2db00715b8)
![ERA_PD - 1](https://github.com/user-attachments/assets/19ee8b36-2ec5-4af2-a632-3f418bec0292)
![ERA_PD - 2](https://github.com/user-attachments/assets/a5d23cd8-a7cb-45fd-be6d-1aaddffbe8cc)
![ERA_PD - 3](https://github.com/user-attachments/assets/e4a244cb-e4a0-4f72-a504-68c7b17173bc)

---

## **Demo Video**
https://github.com/user-attachments/assets/2e0d24dc-e2c5-4b6f-9aa0-3eee5b1c2d94






