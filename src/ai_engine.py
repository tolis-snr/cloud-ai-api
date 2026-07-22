import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# --- PHASE 1: Basic Gemini Setup ---
genai.configure(api_key=api_key)

def generate_summary(text: str) -> str:
    """Uses basic Gemini to summarize text."""
    model = genai.GenerativeModel("gemini-3.1-flash-lite")
    prompt = f"Please summarize the following text:\n{text}"
    response = model.generate_content(contents=prompt)
    return response.text


# --- PHASE 2: RAG Setup (LangChain & ChromaDB) ---
embeddings = GoogleGenerativeAIEmbeddings(google_api_key=api_key, model="models/gemini-embedding-001")
vector_store = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")
llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-3.1-flash-lite", temperature=0)

def save_to_vector_db(text: str, source_name: str):
    """Splits text and saves it to ChromaDB."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    # SKELETON 4: Split Text and Save to Vector DB
    # 1. Split the 'text' argument using text_splitter.split_text()
    # --- WRITE YOUR CODE BELOW ---
    # chunks = ...
    chunks = text_splitter.split_text(text)
    
    # 2. Add chunks to the database using vector_store.add_texts()
    # --- WRITE YOUR CODE BELOW ---
    # ...
    vector_store.add_texts(chunks, metadatas=[{"source": source_name}] * len(chunks))
    
    return f"Knowledge from {source_name} saved successfully!"


def ask_rag_system(question: str) -> dict:
    """Searches DB and asks Gemini to answer based ONLY on the context."""
    
    # SKELETON 5: Retrieve and Answer (RAG)
    # 1. Search DB for relevant chunks using vector_store.similarity_search()
    # --- WRITE YOUR CODE BELOW ---
    # relevant_chunks = ...
    relevant_chunks = vector_store.similarity_search(question, k=3)
    # Explain the code
    # The code above retrieves the top 3 most relevant chunks from the vector database that are similar to the user's question.
    # It uses the `similarity_search` method of the `vector_store` object, which compares the embeddings of the question 
    # with those of the stored text chunks to find the closest matches. 
    # The result is stored in the `relevant_chunks` variable, which will be used to provide context for generating an answer.

    
    # Combine chunks into one string (DO NOT CHANGE THIS LINE)
    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
    
    # 2. Create the STRICT prompt using the 'context' and 'question'
    # --- WRITE YOUR CODE BELOW ---
    # strict_prompt = f"..."
    strict_prompt = f"""Answer the following question based ONLY on the context provided below. 
    If the answer is not in the context, respond with 'I don't know.'\n\nContext:\n{context}\n\nQuestion:\n{question}"""
    
    # 3. Call the LangChain LLM (llm.invoke())
    # --- WRITE YOUR CODE BELOW ---
    # ai_response = ...
    ai_response = llm.invoke(strict_prompt)
    
    return {"answer": ai_response.content, "context_used": context}