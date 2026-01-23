from fastapi import FastAPI
from routes import chat
from services.telegram_bot import start_bot, stop_bot


app = FastAPI()

app.include_router(chat.router)


@app.on_event("startup")
def startup_event():
    start_bot()


@app.on_event("shutdown")
def shutdown_event():
    stop_bot()


if __name__ == "__main__":
    import uvicorn
    from graphs.agent_graph import build_graph

    build_graph()
    uvicorn.run(app, host="0.0.0.0", port=8000)
