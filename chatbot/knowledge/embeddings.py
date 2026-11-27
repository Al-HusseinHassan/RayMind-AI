from langchain_huggingface import HuggingFaceEmbeddings
from chatbot.knowledge.text_splitter import documents_chunked

def get_embedding_model(model_name):
    embedding_model = HuggingFaceEmbeddings(
        model_name = model_name,
        model_kwargs = {"device":"cpu"}
    )
    return embedding_model

def generate_embeddings(embeddings_model, documents_chunk):
    texts = [c.page_content for c in documents_chunk]
    vectors = embeddings_model.embed_documents(texts)
    return vectors



embeddings_model = get_embedding_model("sentence-transformers/all-MiniLM-L6-v2")
embeddings = generate_embeddings(embeddings_model, documents_chunked)