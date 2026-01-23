from langgraph.graph import END
from langgraph.types import Command
from state.GeneralState import GeneralState
from state.OkarinAgentState import OkarinAgentState
from llm_config.model import client


def general_chat_node(state: OkarinAgentState) -> Command:
    """Handle general (non-calendar) chat interactions."""
    user_message = state.user_message

    response = client.invoke(user_message)

    if hasattr(response, "content"):
        response_message = response.content
    else:
        response_message = "I am sorry, I couldn't process your request."

    # response_message = f"Echo: {user_message}"

    return Command(
        update={
            "general_state": GeneralState(
                user_message=user_message,
                response_message=response_message,
            ),
            "draft_response": response_message,
        },
        goto=END,
    )
