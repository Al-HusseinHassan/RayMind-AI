import os
from langchain_chroma import Chroma
from chatbot.knowledge.embeddings import embeddings_model
from chatbot.knowledge.text_splitter import documents_chunked

KNOWLEDGE_PATH = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(KNOWLEDGE_PATH, "chroma_db")

vector_store = Chroma(
    collection_name="respiratory_knowledge",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH
)

# vector_store.add_documents(documents_chunked)