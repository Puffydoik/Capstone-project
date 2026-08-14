from fastapi import FastAPI

from app.graph import graph
from app.schemas import AskRequest, AskResponse

app = FastAPI(
    title="Zepto Support Assistant",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Zepto Support Assistant API is running!"
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):

    result = graph.invoke(
        {
            "query": request.query,
            "intent": "",
            "answer": "",
            "sources": [],
            "confidence": 0.0,
        }
    )

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"],
    )