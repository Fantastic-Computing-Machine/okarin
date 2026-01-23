from llm_config.model import client, model_name
from tools.google_calender import get_calendar_tools
from state import OkarinAgentState
from langchain.agents import create_agent
from node.classify_intent import read_user_message
from langgraph.types import Command
from langgraph.graph import END

_calender_agent = create_agent(
    model=client,
    tools=get_calendar_tools(),
    system_prompt="You are a helpful calendar agent.",
)


def calender_node(state: OkarinAgentState) -> Command[str]:
    """calender node to handle calendar related tasks"""
    response = _calender_agent.invoke(read_user_message(state))

    ai_msg = response["messages"][-1]
    return Command(
        update={
            "draft_response": (
                ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)
            )
        },
        goto=END,
    )
