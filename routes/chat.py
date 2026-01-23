from fastapi import APIRouter
from datamodels.chat import ChatRequest, ChatResponse
from services.chat_service import process_message

router = APIRouter(prefix="/chat")

@router.post("/")
async def chat(
    chat_request: ChatRequest,
):
    reply = process_message(chat_request.message)
    return ChatResponse(reply=reply)
