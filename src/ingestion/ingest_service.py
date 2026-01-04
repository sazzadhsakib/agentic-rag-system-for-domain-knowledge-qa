from fastapi import UploadFile
from ingestion.pdf_loader import parse_pdf_stream
from ingestion.docx_loader import parse_docx_stream
from ingestion.chunker import TextChunker
from ingestion.embeddings import EmbeddingService
import io

class IngestService:
    def __init__(self, store, embedder):
        self.store = store
        self.chunker = TextChunker()
        self.embedder = embedder

    async def ingest_files(self, files: list[UploadFile]):
        total_chunks = 0
        all_texts = []
        all_metadata = []

        for file in files:
            content = await file.read()
            file_stream = io.BytesIO(content)
            text = ""
            filename = file.filename.lower()

            if filename.endswith(".pdf"):
                text = parse_pdf_stream(file_stream)
            elif filename.endswith(".docx"):
                text = parse_docx_stream(file_stream)

            if not text:
                continue

            chunks = self.chunker.chunk(text)

            for chunk in chunks:
                all_texts.append(chunk)
                all_metadata.append({"source": file.filename})
                total_chunks += 1

        if not all_texts:
            return 0

        embeddings = self.embedder.embed(all_texts)
        self.store.upsert(embeddings, all_texts, all_metadata)

        return total_chunks