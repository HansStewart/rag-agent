# RAG Document Intelligence

> A document question-answering system that indexes source content with embeddings, retrieves relevant context with FAISS, and generates grounded answers with GPT-4o.

**by Hans Stewart &nbsp;·&nbsp; [hansstewart.dev](https://hansstewart.dev)**

[Architecture](https://hansstewart.github.io/ai-architecture) &nbsp;·&nbsp; [Portfolio](https://hansstewart.dev) &nbsp;·&nbsp; [GitHub](https://github.com/HansStewart/rag-agent)

---

## What It Does

Documents are split into semantic chunks, embedded, and stored in a FAISS index. When a question arrives, the query is embedded and matched against the index to retrieve the most relevant chunks. Those chunks are injected into the GPT-4o prompt as context — the model generates a response constrained by the indexed source material, not its training data.

**Retrieval pattern:** chunking and embeddings separate knowledge storage from answer generation.  
**Grounding:** retrieved evidence constrains response quality and reduces hallucination risk.  
**Use cases:** internal knowledge systems and private-document Q&A workflows.

---

## Backend Workflow

**Step 1 — Document ingestion** `Input: Documents + source text`
Accepts document content or uploaded source material. Splits the material into manageable semantic chunks. Builds the indexing-ready input set for embedding generation.

**Step 2 — Vector indexing** `Intermediate: FAISS index + chunk map`
Generates OpenAI embeddings for each chunk of the source set. Stores the vectors in a FAISS index for fast semantic retrieval. Preserves document-to-chunk mapping for grounded answer generation.

**Step 3 — Retrieval layer** `Processing: Query → retrieval context`
Embeds the incoming query using the same embedding model. Searches the FAISS index for nearest semantic matches. Packages high-relevance chunks into the prompt context for the model.

**Step 4 — Answer generation** `Output: Grounded document answer`
Injects retrieved chunks into the GPT-4o prompt as context. Generates a response constrained by the indexed source material. Returns a context-grounded answer through the API layer.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | Flask |
| Server | Gunicorn |
| Vector Store | FAISS (local index) |
| Embeddings | OpenAI Embeddings API |
| AI Model | OpenAI GPT-4o |
| Deployment | Google Cloud Run — us-east1 |

---

## Local Development

```bash
git clone https://github.com/HansStewart/rag-agent.git
cd rag-agent
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY to .env
python main.py
# Open http://localhost:8080
```

---

## Project Structure

```
rag-agent/
├── main.py
├── app/
│   ├── __init__.py
│   ├── routes.py          /ingest and /query endpoints
│   ├── ingestor.py        Document splitting and embedding
│   ├── retriever.py       FAISS query and chunk retrieval
│   └── generator.py       GPT-4o grounded answer generation
├── index.html
├── requirements.txt
├── Procfile
└── .env.example           OPENAI_API_KEY=
```

---

## Environment Variables

| Variable | Required | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Embeddings generation + GPT-4o answers |

---

## Full Agent Ecosystem

| Agent | Repository |
|---|---|
| Website Audit Agent | [github.com/HansStewart/website-audit-agent](https://github.com/HansStewart/website-audit-agent) |
| AI Content Pipeline | [github.com/HansStewart/ai-content-pipeline](https://github.com/HansStewart/ai-content-pipeline) |
| Voice-to-CRM Agent | [github.com/HansStewart/voice-to-crm](https://github.com/HansStewart/voice-to-crm) |
| Pipeline Intelligence Agent | [github.com/HansStewart/pipeline-intelligence-agent](https://github.com/HansStewart/pipeline-intelligence-agent) |
| CRM Automation Agent | [github.com/HansStewart/crm-agent](https://github.com/HansStewart/crm-agent) |
| Multi-Agent BI System | [github.com/HansStewart/multi-agent](https://github.com/HansStewart/multi-agent) |
| AI Data Agent | [github.com/HansStewart/ai-data-agent](https://github.com/HansStewart/ai-data-agent) |
| AI Architecture | [hansstewart.github.io/ai-architecture](https://hansstewart.github.io/ai-architecture) |

---

**Hans Stewart &nbsp;·&nbsp; Marketing Automation Engineer &nbsp;·&nbsp; [hansstewart.dev](https://hansstewart.dev)**
