from pydantic import BaseModel, field_validator
from datetime import datetime

class ChatRequest(BaseModel):
    message: str

    @field_validator("message")
    def validate_message(cls, v: str) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M ") + "Asia/Kolkata" + "::" + v


class ChatResponse(BaseModel):
    reply: str
