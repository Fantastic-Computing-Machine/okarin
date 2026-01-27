from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.graph import END
from langgraph.types import Command

from llm_config.model import client
from node.classify_intent import read_user_message
from services.google_todo_service import add_task, complete_task, list_tasks
from state import OkarinAgentState, TodoState
from state.TodoState import agent_todo_instruction_text


@tool
def list_google_tasks() -> str:
    """List pending Google Tasks with numbered IDs for completion."""
    return list_tasks()


@tool
def add_google_task(
    description: str,
    details: str | None = None,
    summary: str | None = None,
    date: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
) -> str:
    """Add a new task with optional details, summary, date, start_time, end_time."""
    return add_task(
        description=description,
        details=details,
        summary=summary,
        date=date,
        start_time=start_time,
        end_time=end_time,
    )


@tool
def complete_google_task(task_number: int) -> str:
    """Complete a Google Task using its number from the list_tasks output."""
    return complete_task(task_number)


_todo_agent = create_agent(
    model=client,
    tools=[list_google_tasks, add_google_task, complete_google_task],
    system_prompt=agent_todo_instruction_text,
)


def todo_node(state: OkarinAgentState) -> Command[str]:
    """Handle to-do intents using Google Tasks tools."""
    response = _todo_agent.invoke(read_user_message(state))
    ai_msg = response["messages"][-1]
    reply_text = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)
    return Command(
        update={
            "todo_state": TodoState(
                user_message=state.user_message,
                response_message=reply_text,
            ),
            "draft_response": reply_text,
        },
        goto=END,
    )
