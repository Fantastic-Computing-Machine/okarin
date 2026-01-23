from pydantic import BaseModel

class GeneralState(BaseModel):
    user_message : str
    response_message : str | None = None
