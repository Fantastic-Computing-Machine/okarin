import sys
sys.path.append(".")

from langgraph.graph.state import CompiledStateGraph

from functools import lru_cache
from langgraph.graph import StateGraph, END
from node.classify_intent import classify_intent
from node.calender_node import calender_node
from node.general_node import general_chat_node
from state.OkarinAgentState import OkarinAgentState
from pathlib import Path
from IPython.display import display, Image


def build_graph(save_png: bool = False):
    agent_graph = StateGraph(OkarinAgentState)
    agent_graph.add_node("ClassifyIntent", classify_intent)
    agent_graph.add_node("CalendarState", calender_node)
    agent_graph.add_node("GeneralState", general_chat_node)  # uncomment if you have it

    agent_graph.set_entry_point("ClassifyIntent")

    def _route_intent(state: OkarinAgentState) -> str:
        """Return a routing key for conditional edges."""
        if state.intent_classification and state.intent_classification.intent == "calendar":
            return "calendar"
        return "general"

    agent_graph.add_conditional_edges(
        "ClassifyIntent",
        _route_intent,
        {
            "calendar": "CalendarState",
            "general": "GeneralState",
        },
    )
    agent_graph.add_edge("CalendarState", END)
    agent_graph.add_edge("GeneralState", END)

    chain: CompiledStateGraph[
        OkarinAgentState, None, OkarinAgentState, OkarinAgentState
    ] = agent_graph.compile()
    if save_png:
        graph_byte = chain.get_graph().draw_mermaid_png()
        output_path: Path = Path("workflow.png")
        output_path.write_bytes(graph_byte)

    return chain


@lru_cache(maxsize=1)
def get_agent_chain():
    """Return a cached compiled graph for runtime use."""
    return build_graph(save_png=False)


if __name__ == "__main__":
    build_graph(save_png=True)
