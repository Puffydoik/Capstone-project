from typing import TypedDict
import chromadb
from langgraph.graph import END, StateGraph
from numpy.ma import ids
from sentence_transformers import SentenceTransformer

from app.config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    MOCK_LLM,
)



model = SentenceTransformer(EMBEDDING_MODEL)

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)



class GraphState(TypedDict):
    query: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float



def classify_intent(state: GraphState):

    query = state["query"].lower()

    keywords = [
    "policy",
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "track",
    "cancel",
    "gift card",
    "support hours",
    "leave",
    "policy",
    ]

    if any(keyword in query for keyword in keywords):
        state["intent"] = "policy_question"
    else:
        state["intent"] = "general_question"

    return state



def retrieve_and_answer(state: GraphState):

    query = state["query"]

    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3,
    )

    docs = results["documents"][0]
    ids = results["ids"][0]

    top_chunk = docs[0]

    if MOCK_LLM:
        answer = top_chunk

    else:
        # Optional real LLM path
        answer = f"LLM answer placeholder using context: {top_chunk[:200]}"

    state["answer"] = answer
    state["sources"] = ids
    state["confidence"] = 1.0

    return state



def direct_answer(state: GraphState):

    if MOCK_LLM:
        state["answer"] = (
            "I can only answer questions about Zepto policies right now."
        )
    else:
        state["answer"] = "LLM direct answer placeholder."

    state["sources"] = []
    state["confidence"] = 1.0

    return state



def router(state: GraphState):

    if state["intent"] == "policy_question":
        return "retrieve"

    return "direct"



builder = StateGraph(GraphState)

builder.add_node("classify_intent", classify_intent)
builder.add_node("retrieve_and_answer", retrieve_and_answer)
builder.add_node("direct_answer", direct_answer)

builder.set_entry_point("classify_intent")

builder.add_conditional_edges(
    "classify_intent",
    router,
    {
        "retrieve": "retrieve_and_answer",
        "direct": "direct_answer",
    },
)

builder.add_edge("retrieve_and_answer", END)
builder.add_edge("direct_answer", END)

graph = builder.compile()