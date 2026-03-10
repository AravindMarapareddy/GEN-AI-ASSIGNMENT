from flask import Flask, render_template, request, jsonify
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# -----------------------------
# Load Documents from docs.json
# -----------------------------

with open("docs.json", "r") as file:
    documents = json.load(file)

doc_texts = [doc["content"] for doc in documents]


# -----------------------------
# Simple Embedding Function
# -----------------------------

def simple_embedding(text):
    return np.array([
        len(text),
        sum(ord(c) for c in text) % 1000
    ])


# -----------------------------
# Generate Document Embeddings
# -----------------------------

doc_embeddings = [simple_embedding(text) for text in doc_texts]


# -----------------------------
# Find Similar Documents
# -----------------------------

def find_similar_docs(query):
    query_words = set(query.lower().split())

    scores = []

    for text in doc_texts:
        doc_words = set(text.lower().split())
        score = len(query_words.intersection(doc_words))
        scores.append(score)

    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:1]

    return [doc_texts[i] for i in top_indices]


# -----------------------------
# Homepage Route
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Chat API
# -----------------------------

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    similar_docs = find_similar_docs(message)

    context = " ".join(similar_docs)

    reply = f"Based on the documents: {context}"

    return jsonify({
        "reply": reply,
        "retrievedChunks": len(similar_docs),
        "tokensUsed": 0
    })


# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)