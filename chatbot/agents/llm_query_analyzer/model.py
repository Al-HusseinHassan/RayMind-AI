from chatbot.agents.llm_query_analyzer.prompts import query_analyzer_prompt
from chatbot.agents.llm_query_analyzer.schema import QueryRoute
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

agent = create_agent(
    model="google_genai:gemini-3.5-flash-lite",
    tools=[],
    system_prompt=query_analyzer_prompt,
    response_format=QueryRoute,
)