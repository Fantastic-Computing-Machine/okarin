from datamodels.chat import ChatRequest
from graphs.agent_graph import get_agent_chain


def process_message(message: str) -> str:
    """
    Run the LangGraph agent pipeline over a user message and return the final response.
    """
    chain = get_agent_chain()

    # LangGraph accepts a dict matching the state schema; we only need the user message.
    result = chain.invoke({"user_message": message})

    # Handle both dict and pydantic model outputs.
    draft_response = None
    if hasattr(result, "draft_response"):
        draft_response = getattr(result, "draft_response")
    elif isinstance(result, dict):
        draft_response = result.get("draft_response")

    if not draft_response:
        return "I'm sorry, I couldn't process your request."

    return draft_response
