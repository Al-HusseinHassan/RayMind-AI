import os
from chatbot.agents.llm_query_analyzer.model import agent
from langchain.messages import HumanMessage
import base64
import mimetypes

def analyze_query(query: str, img_path: str | None = None):

    content = [
        {
            "type": "text",
            "text": query
        }
    ]

    if img_path is not None:
        supported_formats = [".jpg", ".jpeg", ".png"]
        extension = os.path.splitext(img_path)[1].lower()
        if extension not in supported_formats:
            raise ValueError("Unsupported file format. Please upload an image.")
        
        with open(img_path, "rb") as img:
            image_base64 = base64.b64encode(
                img.read()
            ).decode("utf-8")
        mime_type, _ = mimetypes.guess_type(img_path)
        content.append({
            "type": "image",
            "base64": image_base64,
            "mime_type": mime_type
        })

    result = agent.invoke({
        "messages": [
            HumanMessage(content_blocks=content)
        ]
    })

    return result["structured_response"].model_dump()