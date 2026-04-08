from flask import Blueprint, request, jsonify
from app.rag_agent import answer_question, multi_step_analysis
from app.vector_store import add_document, get_store_stats
import PyPDF2
import io

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "RAG Document Intelligence Agent is running!",
        "status": "healthy",
        "endpoints": {
            "POST /upload": "Upload a document (PDF or TXT)",
            "POST /ask": "Ask a question about uploaded documents",
            "POST /analyze": "Deep multi-step analysis on a topic",
            "GET /stats": "Get vector store statistics"
        }
    })

@main.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    filename = file.filename
    try:
        if filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif filename.endswith('.txt'):
            text = file.read().decode('utf-8')
        else:
            return jsonify({"error": "Only PDF and TXT files supported"}), 400
        chunks_added = add_document(text, filename)
        return jsonify({
            "status": "success",
            "message": f"Document '{filename}' indexed successfully!",
            "chunks_created": chunks_added
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Please provide a question"}), 400
    try:
        result = answer_question(data['question'])
        return jsonify({"status": "success", "question": data['question'], **result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/analyze', methods=['POST'])
def analyze_topic():
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "Please provide a topic"}), 400
    try:
        result = multi_step_analysis(data['topic'])
        return jsonify({"status": "success", **result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({"status": "success", **get_store_stats()})