# 📄 RAG Document Intelligence Agent

     

A Retrieval-Augmented Generation (RAG) agent that ingests text documents into a FAISS vector index, performs semantic similarity search, and answers questions strictly from document context with cited sources. Includes a two-pass multi-step analysis mode that extracts themes and generates structured executive reports.

**Live API:** `https://rag-agent-559169459241.us-east1.run.app`

***

## Architecture

```
Document Upload (.txt)
        │
        ▼
┌─────────────────────────────────┐
│       Text Chunker              │
│  splits doc into passages       │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│    OpenAI Embeddings            │
│  text-embedding-ada-002         │
│  each chunk → vector            │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│       FAISS Vector Index        │
│  in-memory · cosine similarity  │
└──────────────────────────────────┘

           Q&A Mode                    Analysis Mode
               │                            │
               ▼                            ▼
    retrieve Top-5 chunks         retrieve Top-8 chunks
               │                            │
               ▼                         Pass 1:
    GPT-4o: answer from              extract 3-5 themes
    context only + [Source X]            │
    citations                         Pass 2:
               │                   GPT-4o: full structured
               ▼                   report using themes +
         JSON response              original context
                                         │
                                         ▼
                                   5-section report
```

***

## Tech Stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.11 |
| Web Framework | Flask 3.0 + Gunicorn |
| Vector Store | FAISS (in-memory) |
| Embeddings | OpenAI text-embedding-ada-002 |
| AI / LLM | OpenAI GPT-4o |
| Containerization | Docker (python:3.11-slim) |
| Cloud | Google Cloud Run — us-east1 |

***

## API Reference

### `POST /upload`
Ingest a document into the FAISS vector index.

**Request:** `multipart/form-data`
```
file: document.txt
```

**Response:**
```json
{
  "message": "Document uploaded and indexed successfully",
  "chunks_created": 24
}
```

***

### `POST /ask`
Ask a question — answered strictly from indexed document context with source citations.

**Request:**
```json
{ "question": "What are the main findings?" }
```

**Response:**
```json
{
  "answer": "The main findings include... [Source 1] [Source 3]",
  "sources": ["chunk_1", "chunk_3"],
  "chunks_used": 5
}
```

***

### `POST /analyze`
Two-pass deep analysis on a topic using the indexed documents.

**Request:**
```json
{ "topic": "market expansion strategy" }
```

**Response:**
```json
{
  "topic": "market expansion strategy",
  "themes": ["Theme 1", "Theme 2", "Theme 3"],
  "report": {
    "executive_summary": "...",
    "key_findings": "...",
    "detailed_analysis": "...",
    "recommendations": "...",
    "conclusion": "..."
  },
  "sources": ["chunk_2", "chunk_5", "chunk_8"],
  "chunks_analyzed": 8
}
```

***

## How It Works

### Q&A Mode (`/ask`)
1. User submits a question
2. Question is embedded via OpenAI `text-embedding-ada-002`
3. FAISS performs cosine similarity search → returns Top-5 most relevant chunks
4. Chunks are formatted as `[Source 1]...[Source 5]` context string
5. GPT-4o is instructed to answer **only from the provided context** — no hallucination
6. Response includes the answer and which source chunks were used

### Multi-Step Analysis Mode (`/analyze`)
**Pass 1 — Theme Extraction:**
- Top-8 chunks retrieved from FAISS
- GPT-4o extracts 3–5 key themes from the document corpus

**Pass 2 — Structured Report:**
- Themes + original chunks sent to GPT-4o together
- GPT-4o generates a full report: Executive Summary → Key Findings → Detailed Analysis → Recommendations → Conclusion

***

## Local Setup

```bash
git clone https://github.com/HansStewart/rag-agent.git
cd rag-agent
pip install -r requirements.txt
```

Create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

Run the server:
```bash
python main.py
```

Test with the sample document:
```bash
# Upload
curl -X POST http://localhost:5000/upload \
  -F "file=@sample.txt"

# Ask
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

***

## Project Structure

```
rag-agent/
├── app/
│   ├── rag_agent.py      # Q&A + multi-step analysis logic
│   ├── vector_store.py   # FAISS indexing + semantic search
│   └── routes.py         # Flask endpoints
├── main.py               # App entry point
├── sample.txt            # Sample document for testing
├── Dockerfile
└── requirements.txt
```

***

## Deployment

```bash
gcloud run deploy rag-agent \
  --source . \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated
```

***

## Part of the AI Agent Portfolio

| Agent | Description | Live URL |
|---|---|---|
| AI Data Agent | CSV analysis + GPT-4o insights | [↗](https://ai-data-agent-559169459241.us-east1.run.app) |
| **RAG Document Intelligence** | FAISS vector search + cited Q&A | [↗](https://rag-agent-559169459241.us-east1.run.app) |
| CRM Automation Agent | HubSpot + lead scoring + email gen | [↗](https://crm-agent-559169459241.us-east1.run.app) |
| Multi-Agent BI System | CrewAI 4-agent pipeline | [↗](https://multi-agent-559169459241.us-east1.run.app) |

**Author:** [Hans Stewart](https://github.com/HansStewart)