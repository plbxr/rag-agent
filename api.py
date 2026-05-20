"""
FastAPI 接口 - 将Agent包装为Web API
"""
from fastapi import FastAPI
from pydantic import BaseModel
from rag_agent import RAGAgent

app = FastAPI(title="RAG Agent API")
agent = RAGAgent()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """对话接口"""
    reply = agent.chat(req.message)
    return ChatResponse(reply=reply)


@app.post("/clear")
def clear():
    """清空对话历史"""
    agent.clear_history()
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
