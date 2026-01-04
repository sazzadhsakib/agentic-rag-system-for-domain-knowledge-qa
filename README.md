# Agentic RAG System for Domain Knowledge QA



An intelligent, Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **Azure OpenAI**, and **Qdrant**. This system goes beyond simple "chat with PDF" by implementing **Agentic Behavior**—it reflects on its own answers, rewrites queries if necessary, and understands both text and images from documents.

## 🚀 Key Features

* **🧠 Agentic Reasoning:** Uses a "Retrieve-Reflect-Rewrite" loop. If the agent finds retrieved context insufficient, it automatically rewrites the search query to find better results.
* **👁️ Multimodal Ingestion:** Automatically extracts and **captions images** from PDFs and DOCX files using GPT-4o-mini, making charts and diagrams searchable.
* **🔄 Contextual Chat:** Supports conversation history, allowing users to ask follow-up questions (e.g., "Where are they located?" after asking about specific people).
* **📂 Multi-Format Support:** Ingests both `.pdf` and `.docx` files.
* **⚡ High Performance:** Built on FastAPI (Async) and Qdrant (Rust-based Vector DB).
* **🐳 Dockerized:** One-command deployment.

## 🛠️ Tech Stack

* **LLM & Embeddings:** Azure OpenAI (GPT-4o-mini, Ada-002)
* **Vector Database:** Qdrant
* **Backend:** FastAPI, Pydantic
* **Document Parsing:** PyMuPDF (PDFs), Python-Docx
* **Containerization:** Docker & Docker Compose

## 📂 Project Structure

```bash
.
├── src
│   ├── agent           # Logic for Reflection, Query Rewriting, and Answer Generation
│   ├── api             # FastAPI Routes and Pydantic Schemas
│   ├── config          # Environment variable management
│   ├── ingestion       # PDF/DOCX Loaders, Chunking, and Image Captioning
│   ├── llm             # Azure OpenAI Wrapper
│   ├── retrieval       # Search logic
│   ├── vectorstore     # Qdrant Client wrapper
│   └── app.py          # Application Entrypoint
├── .env                # API Keys and Config (Not committed)
├── .gitignore
├── docker-compose.yml  # Container orchestration
├── Dockerfile          # Image definition
├── requirements.txt    # Python dependencies
└── LICENSE             # MIT License

```

## ⚙️ Configuration

Create a `.env` file in the root directory:

```ini
# Azure OpenAI Credentials
AZURE_OPENAI_ENDPOINT=[https://your-resource-name.cognitiveservices.azure.com/](https://your-resource-name.cognitiveservices.azure.com/)
AZURE_OPENAI_KEY=your_api_key_here

# Deployment Names (Check your Azure Studio)
AZURE_DEPLOYMENT_CHAT=gpt-4o-mini
AZURE_API_VERSION_CHAT=2025-01-01-preview

AZURE_DEPLOYMENT_EMBED=text-embedding-ada-002
AZURE_API_VERSION_EMBED=2023-05-15

# Vector Database (Docker uses 'qdrant', Local uses 'localhost')
QDRANT_URL=http://qdrant:6333
QDRANT_COLLECTION=rag_collection

```

---

## 🏃‍♂️ How to Run

### Option A: Using Docker (Recommended)

This sets up both the API and the Vector Database automatically.

```bash
docker-compose up --build

```

* **API:** `http://localhost:8000`
* **Swagger UI:** `http://localhost:8000/docs`

### Option B: Running Locally

1. **Start Qdrant:**
```bash
docker run -p 6333:6333 qdrant/qdrant

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run API:**
*Update `.env` to set `QDRANT_URL=http://localhost:6333` first.*
```bash
cd src
uvicorn app:app --reload

```



---

## 📡 API Usage

### 1. Ingest Documents

Upload PDFs or DOCX files to the knowledge base.

```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@./path/to/article.pdf" \
  -F "files=@./path/to/notes.docx"

```

### 2. Ask a Question

Send a query to the agent.

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this paper about?",
    "top_k": 5,
    "history": []
  }'

```

```

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

```