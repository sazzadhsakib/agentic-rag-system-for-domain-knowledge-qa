from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from api.schemas import AskRequest, AskResponse
from ingestion.ingest_service import IngestService
from ingestion.embeddings import EmbeddingService
from vectorstore.qdrant_store import QdrantStore
from retrieval.retriever import Retriever
from llm.azure_openai import AzureLLM
from agent.rag_agent import RAGAgent
from config.settings import QDRANT_URL, QDRANT_COLLECTION, VECTOR_DIM


router = APIRouter()

embedder = EmbeddingService()
store = QdrantStore(QDRANT_URL, QDRANT_COLLECTION, VECTOR_DIM)
ingest_service = IngestService(store, embedder)
retriever = Retriever(store, embedder)
llm = AzureLLM()
agent = RAGAgent(retriever, llm)

@router.post("/ingest")
async def ingest(files: List[UploadFile] = File(...)):
    """
    Uploads one or more PDF files, extracts text, chunks it, and stores embeddings.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    try:
        count = await ingest_service.ingest_files(files)
        return {
            "status": "success",
            "files_processed": len(files),
            "chunks_ingested": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    answer, sources = agent.answer(request.question, request.top_k)
    return AskResponse(answer=answer, sources=sources)


@router.delete("/documents/{filename}")
def delete_document(filename: str):
    """
    Removes all chunks associated with a specific filename.
    """
    try:
        store.delete_file(filename)
        return {"status": "success", "message": f"Deleted {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reset")
def reset_db():
    try:
        store.reset()
        return {"status": "success", "message": "Vector store has been reset and recreated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")