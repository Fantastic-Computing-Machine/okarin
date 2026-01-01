from fastapi import APIRouter
from agent_factory.chat_agent import get_agent
from datamodels.chat import ChatRequest, ChatResponse
from langchain.messages import AIMessage, HumanMessage

router = APIRouter(prefix="/chat")

@router.post("/")
async def chat(
    chat_request: ChatRequest,
):
    agent = get_agent()
    reply = agent.agent.invoke(
        {"messages": [{"role": "user", "content": chat_request.message}]}
    )
    if reply is None or not reply.get("messages", []):
        reply = "I'm sorry, I couldn't process your request."
    else:
        reply = reply.get("messages", [])[-1].content
    return ChatResponse(reply=reply)
