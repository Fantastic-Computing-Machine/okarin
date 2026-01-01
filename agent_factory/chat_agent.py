from llm_config.model import client, model_name
from langchain.agents import create_agent
from tools.google_calender import get_calendar_tools

_agent_instance = None


class ChatAgent:
    def __init__(self):
        self.client = client
        self.model_name = model_name
        self.agent = create_agent(
            model=client,
            tools=get_calendar_tools(),
            system_prompt="You're a helpful chat agent.",
        )


def get_agent() -> "ChatAgent":
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ChatAgent()
    return _agent_instance
