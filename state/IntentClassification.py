from typing import Literal
from pydantic import BaseModel

class IntentClassification(BaseModel):
    intent : Literal["email","calendar","notes","todo", "web_search","general_chat","add_knowledge_base"]
    confidence: float
    details: str | None = None