from openai import OpenAI
from dotenv import load_dotenv
import os
from app.vector_store import search_documents

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def answer_question(question):
    relevant_chunks = search_documents(question, top_k=5)
    if not relevant_chunks:
        return {
            "answer": "No documents uploaded yet. Please upload documents first.",
            "sources": [],
            "chunks_used": 0
        }
    context = ""
    sources_used = []
    for i, result in enumerate(relevant_chunks):
        context += f"\n[Source {i+1}: {result['source']}]\n{result['chunk']}\n"
        if result['source'] not in sources_used:
            sources_used.append(result['source'])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are an expert document analyst.
                Answer questions based ONLY on the provided context.
                Always cite sources using [Source X] notation.
                If the answer cannot be found, say so clearly."""
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        max_tokens=1500
    )
    return {
        "answer": response.choices[0].message.content,
        "sources": sources_used,
        "chunks_used": len(relevant_chunks)
    }

def multi_step_analysis(topic):
    initial_results = search_documents(topic, top_k=8)
    if not initial_results:
        return {"error": "No documents available for analysis"}
    context = "\n".join([f"[{r['source']}]: {r['chunk']}" for r in initial_results])
    themes_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Extract the 3-5 key themes from the provided context."},
            {"role": "user", "content": f"Extract key themes from:\n{context}"}
        ],
        max_tokens=500
    )
    themes = themes_response.choices[0].message.content
    report_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """Create a comprehensive analysis report with:
                Executive Summary, Key Findings, Detailed Analysis,
                Recommendations, and Conclusion."""
            },
            {
                "role": "user",
                "content": f"Topic: {topic}\n\nThemes:\n{themes}\n\nContext:\n{context}"
            }
        ],
        max_tokens=2000
    )
    return {
        "topic": topic,
        "themes": themes,
        "report": report_response.choices[0].message.content,
        "sources": list(set([r['source'] for r in initial_results])),
        "chunks_analyzed": len(initial_results)
    }