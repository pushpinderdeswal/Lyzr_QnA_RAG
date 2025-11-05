# Lyzr Clinic QnA  
**AI-Powered Clinic Assistant** – Ask anything about location, hours, insurance, parking… and it **remembers context**!

> **"Where is the clinic?" → "What about parking?"** → **Understands reference!**

---

## Features

| Feature | Description |
|--------|-----------|
| **Context-Aware** | Remembers previous questions |
| **Per-User Sessions** | No cross-talk between users |
| **FastAPI + LangChain** | Production-ready RAG |
| **Docker Support** | One command to run |
| **Clear Chat** | Reset anytime |

---

## Tech Stack

```text
Backend: FastAPI + LangChain + OpenAI
Embeddings: text-embedding-3-small
Vector DB: Chroma (persistent)
Deployment: Docker + docker-compose
```

---

## Installation & Running

### Option 1: With Docker (Recommended)

```bash
# 1. Clone repo
git clone https://github.com/yourname/lyzr-clinic-qna.git
cd lyzr-clinic-qna

# 2. Copy .env.example → .env and add your OpenAI key
cp .env.example .env
# Edit .env: OPENAI_API_KEY=sk-...

# 3. Run (first time builds + ingests)
docker compose up --build

# 4. Later runs (fast!)
docker compose up
```

Open: [http://localhost:8000](http://localhost:8000)

---

### Option 2: Without Docker (Local)

```bash
# 1. Clone and enter
git clone https://github.com/yourname/lyzr-clinic-qna.git
cd lyzr-clinic-qna

# 2. Create virtual env
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. Install deps
pip install -r requirements.txt

# 4. Set up .env
cp .env.example .env
# Edit: add OPENAI_API_KEY

# 5. Ingest FAQ data
python scripts/ingest.py

# 6. Run server
uvicorn main:app --reload
```

Open: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Demo Videos

### General Chat Demo  

*Ask about hours, insurance, location — instant answers!*

[Watch Demo Video](https://github.com/pushpinderdeswal/Lyzr_QnA_RAG/releases/download/1.0/Screen.Recording.2025-11-05.at.10.36.54.PM.mov)

---

### Context Awareness Demo  

*"Where is the clinic?" → "What about parking?" → Understands reference!*

[Watch Demo Video](https://github.com/pushpinderdeswal/Lyzr_QnA_RAG/releases/download/1.0/Screen.Recording.2025-11-05.at.10.39.39.PM.mov)

---

## Project Structure

```bash
clinic-faq-rag/
├── data/clinic_info.json        FAQ source
├── vector_db/                   Chroma DB (auto-created)
├── templates/index.html         UI
├── scripts/ingest.py            Ingest script
├── api/qna.py                   FastAPI routes
├── models/rag.py                RAG chain + memory
├── services/vector_store.py     Chroma retriever
├── main.py                      App entry
├── Dockerfile
├── docker-compose.yml
└── .env                         Your OpenAI key
```

---

## Environment Variables (`.env`)

```env
OPENAI_API_KEY=sk-your-real-key-here
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
COLLECTION_NAME=clinic_faqs
```

---

## Development

```bash
# Hot reload (no Docker)
uvicorn main:app --reload

# Re-ingest data
python scripts/ingest.py
```

---
