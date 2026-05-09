from fastapi import FastAPI
from app.models import ChatRequest, ChatResponse
from app.catalog import load_catalog
from app.retrieval import CatalogRetriever
from app.agent import chat_agent

app = FastAPI(title="SHL Assessment Recommender")

catalog = load_catalog()
retriever = CatalogRetriever(catalog)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = chat_agent(request.messages, retriever)
    return result