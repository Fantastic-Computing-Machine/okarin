from typing import Literal
from langgraph.graph import StateGraph, END
from langchain.messages import AIMessage, HumanMessage
from state import OkarinAgentState, IntentClassification
from llm_config.model import client
from langgraph.types import Command

def read_user_message(state: OkarinAgentState) -> dict:
    """Adapt state to the input schema expected by LangChain agents (messages list)."""
    return {"messages": [HumanMessage(content=state.user_message)]}


def classify_intent(state:OkarinAgentState):
    """ classify the intent of the user message """
    print("Inside classify_intent with user_message:", state.user_message)
    structured_llm = client.with_structured_output(IntentClassification)
    classification_prompt  = f"""
        You are an intent classification model. Classify the intent of the user message.
        user_message: {state.user_message}
        provide the intent as one of the following: "email","calendar","notes","todo", "web_search","general_chat","add_knowledge_base"
    """

    classification:IntentClassification = structured_llm.invoke(classification_prompt) # type: ignore

    print("classification:", classification)

    if classification.intent == "calendar":
        goto = "CalendarState"
    else:
        # Route everything else to general chat for now.
        goto = "GeneralState"

    updates: dict[str, IntentClassification] = {"intent_classification": classification}

    return Command(update=updates, goto=goto)
