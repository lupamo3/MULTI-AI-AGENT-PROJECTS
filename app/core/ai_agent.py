# app/core/ai_agent.py
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

from app.config.settings import settings

load_dotenv()


def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    # 1. LLM setup
    llm = ChatGroq(
        model=llm_id,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    # 2. Tools (keep Tavily off for now if you want)
    tools = []
    if allow_search:
        # If your TAVILY_API_KEY is correctly set, you can re-enable this:
        # tools = [TavilySearchResults(max_results=2)]
        tools = []

    # 3. Create the agent – NOTE: no state_modifier anymore
    agent = create_react_agent(
        model=llm,
        tools=tools,
    )

    # 4. Inject system prompt into the first message
    if system_prompt:
        combined_text = f"{system_prompt.strip()}\n\nUser query: {query}"
    else:
        combined_text = query

    state = {
        "messages": [HumanMessage(content=combined_text)]
    }

    # 5. Call agent and extract latest AI message
    response = agent.invoke(state)

    messages = response.get("messages", [])
    ai_messages = [
        m.content for m in messages
        if isinstance(m, AIMessage)
    ]

    return ai_messages[-1] if ai_messages else "No response from agent."
