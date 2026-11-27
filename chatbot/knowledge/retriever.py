from chatbot.knowledge.vector_store import vector_store

def build_filter(metadata):

    filter = []

    if metadata["sections"]:
        filter.append({
            "section": {"$in": metadata["sections"]}
        })

    if metadata["diseases"]:
        filter.append({
            "disease": {"$in": metadata["diseases"]}
        })

    if not filter:
        return None

    if len(filter) == 1:
        return filter[0]

    return {"$and": filter}

def retrieve_documents(query, k=4, metadata_filter=None):
    retrieved_documents = vector_store.similarity_search(
        query,
        k=k,
        filter= metadata_filter
    )
    return retrieved_documents