import base64
from openai import AzureOpenAI
from config.settings import (
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_API_VERSION_CHAT,
    AZURE_DEPLOYMENT_CHAT
)

class AzureLLM:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_API_VERSION_CHAT
        )
        self.deployment = AZURE_DEPLOYMENT_CHAT

    def chat(self, messages: list, temperature: float = 0):
        """
        Standard chat completion for text generation.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Azure Chat Error: {e}")
            return f"Error communicating with AI: {str(e)}"

    def describe_image(self, image_bytes: bytes) -> str:
        """
        Sends raw image bytes to the model for captioning/description.
        Used during ingestion to convert PDF images into searchable text.
        """
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical documentation assistant. Your job is to describe images found in documents so that their content can be indexed for search. Focus on extracting text inside the image, describing charts/graphs trends, and identifying key visual elements."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe this image in detail for a blind user or search index."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "auto"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300,
                temperature=0.3
            )
            print (response)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Image captioning failed: {e}")
            return "[Image description unavailable due to error]"