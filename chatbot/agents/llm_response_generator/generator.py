from chatbot.agents.llm_response_generator.model import get_model_generation
from chatbot.agents.llm_response_generator.model import Build_Human_message_to_model_generation



def final_generation(thread_id, query, image_path:str|None = None):

    model_input = Build_Human_message_to_model_generation(query, image_path)
    model = get_model_generation()

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print("--------------------------===================--------------------==================-------------------")
    for chunk, metadata in model.stream(
        {"messages": [model_input]},
        config=config,
        stream_mode="messages"
    ):
        if chunk.content:
            if isinstance(chunk.content, str):
                yield chunk.content
            else:
                for block in chunk.content:
                    if block.get("type") == "text":
                        yield block["text"]
    print("--------------------------===================--------------------==================-------------------")
