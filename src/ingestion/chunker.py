import tiktoken

class TextChunker:
    def __init__(self, chunk_size=400, overlap=60):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def chunk(self, text: str):
        tokens = self.encoder.encode(text)
        chunks = []

        start = 0
        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunks.append(self.encoder.decode(chunk_tokens))
            start += self.chunk_size - self.overlap

        return chunks
