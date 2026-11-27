from chatbot.knowledge.retriever import build_filter, retrieve_documents
from chatbot.agents.llm_query_analyzer.agent import analyze_query
from machine_learning_model.prediction import final_prediction
    
def trigger(query: str, metadata: dict, img_path: str | None = None):

    # Retrieve relevant documents
    metadata_filter = build_filter(metadata)
    retrieved_documents = retrieve_documents(
        query,
        4,
        metadata_filter
    )

    # Run ML prediction if an image and modality are available
    prediction_response = None

    if metadata.get("modality") is not None and img_path is not None:
        prediction_response = final_prediction(
            img_path,
            metadata["modality"]
        )


    return {
        "retrieved_documents": retrieved_documents,
        "prediction": prediction_response
    }