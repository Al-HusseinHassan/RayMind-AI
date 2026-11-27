from langchain_text_splitters import RecursiveCharacterTextSplitter
from chatbot.knowledge.document_loader import documents_page_level

def splitting_documents(documents_page_level):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap=150,
        length_function = len,
        separators=["\n\n", "\n", " ", ""]
    )
    documents_chunked = text_splitter.split_documents(documents_page_level)
    return documents_chunked

documents_chunked = splitting_documents(documents_page_level)