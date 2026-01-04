from openai import AzureOpenAI
from config.settings import (
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_API_VERSION_EMBED,
    AZURE_DEPLOYMENT_EMBED
)

class EmbeddingService:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_API_VERSION_EMBED
        )
        self.deployment = AZURE_DEPLOYMENT_EMBED

    def embed(self, texts: list[str]):
        cleaned_texts = [t.replace("\n", " ") for t in texts]

        response = self.client.embeddings.create(
            input=cleaned_texts,
            model=self.deployment
        )
        return [data.embedding for data in response.data]