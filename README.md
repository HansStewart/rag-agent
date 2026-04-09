# 🤖 RAG Document Intelligence Agent

A production-ready Retrieval-Augmented Generation (RAG) system that ingests documents, stores them in a vector database, and answers questions with cited sources.

| [rag-agent](https://github.com/HansStewart/rag-agent) | Document Q&A with FAISS vector search | [Live](https://rag-agent-559169459241.us-east1.run.app) |

## 🌐 Live API
https://rag-agent-559169459241-us-east1.run.app 

## 🛠️ Tech Stack
- Python 3.14 — Core language
- Flask — REST API framework
- OpenAI GPT-4o — AI reasoning engine
- OpenAI Embeddings — text-embedding-3-small
- FAISS — Vector database for similarity search
- LangChain — Document processing
- GCP Cloud Run — Cloud deployment

## 🚀 Features
- Upload PDF or TXT documents via REST API
- Automatic text chunking and embedding
- FAISS vector similarity search
- AI answers with cited sources
- Multi-step deep analysis reports
- Production deployed on GCP

## 📦 Installation

1. Clone the repository
git clone https://github.com/HansStewart/rag-agent.git
cd rag-agent

2. Create virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Add your API key
Create .env file:
OPENAI_API_KEY=your_key_here

5. Run the app
python main.py

## 🧪 API Endpoints

GET  /          - Health check
POST /upload    - Upload PDF or TXT document
POST /ask       - Ask a question with cited answers
POST /analyze   - Deep multi-step topic analysis
GET  /stats     - Vector store statistics

## 💡 How RAG Works
Document Upload → Text Chunking → OpenAI Embeddings →
FAISS Vector Store → Similarity Search → GPT-4o Answer + Citations

## 🏗️ Project Structure
rag-agent/
├── app/
│   ├── __init__.py       - Flask app factory
│   ├── routes.py         - API endpoints
│   ├── rag_agent.py      - AI agent + multi-step analysis
│   └── vector_store.py   - FAISS vector database
├── documents/            - Document storage
├── main.py               - Entry point
├── requirements.txt      - Dependencies
├── Dockerfile            - Container config
└── README.md             - Documentation

## 👤 Author
Hans Stewart
GitHub: https://github.com/HansStewart