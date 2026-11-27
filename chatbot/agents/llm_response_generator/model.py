from dotenv import load_dotenv
from langchain.agents import create_agent
from chatbot.agents.llm_query_analyzer.agent import analyze_query
from chatbot.agents.trigger.trigger import trigger
from chatbot.agents.llm_response_generator.prompt import response_generator_prompt
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage

load_dotenv()

checkpointer = InMemorySaver()

model = create_agent(
    model = "google_genai:gemini-3.5-flash-lite",
    system_prompt=response_generator_prompt,
    checkpointer = checkpointer
)

def get_model_generation():
    return model

def Build_Human_message_to_model_generation(query, image_path:str|None = None):
    metadata = analyze_query(query, image_path)
    retrieval_prediction = trigger(query, metadata, image_path)

    combined_message = f"""
    User Query:
    {query}

    Metadata:
    {metadata}

    ML Prediction:
    {retrieval_prediction["prediction"]}

    Retrieved Documents:
    {retrieval_prediction["retrieved_documents"]}
    """

    return HumanMessage(content=combined_message)
