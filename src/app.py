from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Agentic RAG API",
    description="Azure OpenAI + Qdrant based RAG system",
    version="1.0.0"
)

app.include_router(router)
