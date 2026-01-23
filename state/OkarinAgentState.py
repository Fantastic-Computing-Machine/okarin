from pydantic import BaseModel
from state.IntentClassification import IntentClassification
from state.CalenderState import CalenderState
from state.GeneralState import GeneralState
from typing import Optional

class OkarinAgentState(BaseModel):
    user_message: str

    intent_classification: Optional[IntentClassification] = None

    # states
    calender_state: Optional[CalenderState] = None
    general_state: Optional[GeneralState] = None
    send_email_state: Optional[BaseModel] = None
    todo_state: Optional[BaseModel] = None
    web_search_state: Optional[BaseModel] = None
    knowledge_base_state: Optional[BaseModel] = None

    draft_response: Optional[str] = None
    message: list[str] | None = None
    error_message: Optional[str] = None
