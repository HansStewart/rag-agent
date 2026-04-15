━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  RAG DOCUMENT INTELLIGENCE
  Source documents indexed with embeddings. Questions answered by
  GPT-4o — grounded entirely in your content.
  by Hans Stewart · hansstewart.dev

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Architecture    →   hansstewart.github.io/ai-architecture
  Portfolio       →   hansstewart.dev
  GitHub          →   github.com/HansStewart/rag-agent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IT DOES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  A document question-answering system that indexes source content with
  OpenAI embeddings, retrieves relevant context with FAISS, and generates
  grounded answers with GPT-4o.

  Documents are split into semantic chunks, embedded, and stored in a
  FAISS index. When a question arrives, the query is embedded and
  matched against the index to retrieve the most relevant chunks. Those
  chunks are injected into the GPT-4o prompt as context — the model
  generates a response constrained by the indexed source material, not
  its training data.

  Retrieval pattern: chunking and embeddings separate knowledge storage
  from answer generation. Grounding: retrieved evidence constrains
  response quality and reduces hallucination risk. Use cases: internal
  knowledge systems and private-document Q&A workflows.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BACKEND WORKFLOW — 4 STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Step 01 — Document ingestion
    Accepts document content or uploaded source material.
    Splits the material into manageable semantic chunks.
    Builds the indexing-ready input set for embedding generation.
    → Input: Documents + source text

  Step 02 — Vector indexing
    Generates OpenAI embeddings for each chunk of the source set.
    Stores the vectors in a FAISS index for fast semantic retrieval.
    Preserves document-to-chunk mapping for grounded answer generation.
    → Intermediate: FAISS index + chunk map

  Step 03 — Retrieval layer
    Embeds the incoming query using the same embedding model.
    Searches the FAISS index for nearest semantic matches.
    Packages high-relevance chunks into the prompt context for the model.
    → Processing: Query → retrieval context

  Step 04 — Answer generation
    Injects retrieved chunks into the GPT-4o prompt as context.
    Generates a response constrained by the indexed source material.
    Returns a context-grounded answer through the API layer.
    → Output: Grounded document answer


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECH STACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Language        Python 3.11
  Framework       Flask
  Server          Gunicorn
  Vector Store    FAISS (local index)
  Embeddings      OpenAI Embeddings API
  AI Model        OpenAI GPT-4o (answer generation)
  Deployment      Google Cloud Run — us-east1


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOCAL DEVELOPMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  git clone https://github.com/HansStewart/rag-agent.git
  cd rag-agent
  pip install -r requirements.txt
  cp .env.example .env
  → Add OPENAI_API_KEY to .env
  python main.py
  → Open http://localhost:8080


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROJECT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  rag-agent/
  ├── main.py
  ├── app/
  │   ├── __init__.py
  │   ├── routes.py              /ingest and /query endpoints
  │   ├── ingestor.py            Document splitting and embedding
  │   ├── retriever.py           FAISS query and chunk retrieval
  │   └── generator.py           GPT-4o grounded answer generation
  ├── index.html
  ├── requirements.txt
  ├── Procfile
  └── .env.example               OPENAI_API_KEY=


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENVIRONMENT VARIABLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OPENAI_API_KEY       required    Embeddings generation + GPT-4o answers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Hans Stewart · Marketing Automation Engineer · hansstewart.dev
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━