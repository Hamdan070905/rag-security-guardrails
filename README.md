# 🔒 SecureRAG — Enterprise AI Document Intelligence

![Python](https://img.shields.io/badge/Python-3.11-blue)
![AI](https://img.shields.io/badge/AI-Llama3-green)
![Security](https://img.shields.io/badge/Security-3%20Layers-red)

## 🎯 What It Does
Upload any PDF → Ask questions → Get AI answers
with enterprise security guardrails

## ✨ Features
- ✅ Vector search (ChromaDB + MiniLM)
- ✅ Prompt injection detection
- ✅ Toxic content filtering  
- ✅ Audit logging with timestamps
- ✅ Grounded answers (no hallucination)
- ✅ Source chunk transparency

## 🏗️ Architecture
PDF → Extract → Chunk → Embed → Store
Query → Security Check → Vector Search → LLM → Answer

## 🔧 Tech Stack
| Component | Technology |
|-----------|-----------|
| AI Model | Llama 3 / Claude |
| Vector DB | ChromaDB |
| Embeddings | Sentence Transformers |
| UI | Gradio |
| Security | Custom Guardrails |

## 🚀 Run Locally
pip install -r requirements.txt
python app.py

## 🔑 Environment Variables
GROQ_API_KEY=your_key
ANTHROPIC_API_KEY=your_key