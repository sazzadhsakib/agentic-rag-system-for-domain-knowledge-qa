from pydantic import BaseModel
from typing import List

class IngestRequest(BaseModel):
    directory: str

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

class SourceChunk(BaseModel):
    source: str
    text: str

class AskResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
