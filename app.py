import gradio as gr
import os
from rag_engine import extract_text_from_pdf, store_document, retrieve_relevant_chunks, ask_claude
from security import run_security_checks
from logger import log_query, get_all_logs

doc_loaded = {"status": False}

def process_pdf(pdf_file):
    if pdf_file is None:
        return "⚠️ Please upload a PDF file first."
    try:
        text, error = extract_text_from_pdf(pdf_file.name)
        if error:
            return f"❌ {error}"
        
        word_count = len(text.split())
        char_count = len(text)
        chunks = store_document(text, "document")
        doc_loaded["status"] = True
        
        return f"""✅ Document processed successfully!
        
📊 Statistics:
- Words extracted: {word_count:,}
- Characters: {char_count:,}  
- Chunks created: {chunks}
- Embedding model: MiniLM-L6-v2
- Vector DB: ChromaDB
- Status: Ready for queries"""
    except Exception as e:
        return f"❌ Error: {str(e)}"

def answer_question(query):
    if not query or not query.strip():
        return "⚠️ Please enter a question.", ""
    if not doc_loaded["status"]:
        return "⚠️ Upload and process a PDF first!", ""
    
    is_safe, security_msg = run_security_checks(query)
    log_query(query, is_safe, security_msg)
    
    if not is_safe:
        return f"🚨 BLOCKED: {security_msg}", ""
    
    try:
        chunks = retrieve_relevant_chunks(query)
        answer = ask_claude(query, chunks)
        
        # Show sources
        sources = "\n\n---\n".join(
            [f"📄 Source {i+1}:\n{chunk[:200]}..." 
             for i, chunk in enumerate(chunks)]
        )
        return answer, sources
    except Exception as e:
        return f"❌ Error: {str(e)}", ""

def get_logs():
    logs = get_all_logs()
    if not logs:
        return "No queries logged yet."
    output = ""
    for log in logs[-10:]:
        status = "✅ SAFE" if log['security_passed'] else "🚨 BLOCKED"
        output += f"[{log['timestamp']}] {status} | {log['query'][:60]}\n"
    return output

css = """
* {font-family: 'Segoe UI', sans-serif !important;}
.gradio-container {max-width: 1100px !important; margin: auto !important;}
footer {display: none !important;}

.main-header {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #0f3460;
    padding: 28px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 16px;
}

.badge-row {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.badge {
    background: #0f3460;
    color: #4cc9f0;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 12px;
    border: 1px solid #4cc9f0;
}

.security-box {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 16px;
    margin-top: 10px;
}

.security-item {
    color: #3fb950;
    margin: 6px 0;
    font-size: 13px;
}

.arch-box {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 20px;
    color: #8b949e;
    font-size: 13px;
    line-height: 1.8;
}
"""

with gr.Blocks(title="SecureRAG AI") as app:

    gr.HTML("""
    <div class="main-header">
        <h1 style="color:#e6edf3; margin:0; font-size:26px;">🔒 SecureRAG — Enterprise Document Intelligence</h1>
        <p style="color:#8b949e; margin:8px 0 0 0; font-size:14px;">
            Vector Search • Claude AI • Security Guardrails • Audit Logging
        </p>
    </div>
    <div class="badge-row">
        <span class="badge">✅ Injection Guard</span>
        <span class="badge">✅ Toxic Filter</span>
        <span class="badge">✅ Audit Trail</span>
        <span class="badge">✅ Vector Search</span>
        <span class="badge">✅ Claude AI</span>
    </div>
    """)

    with gr.Tabs():

        with gr.Tab("📄 Document Q&A"):
            with gr.Row():

                with gr.Column(scale=1):
                    gr.Markdown("### 📁 Upload Document")
                    pdf_input = gr.File(
                        label="Upload PDF",
                        file_types=[".pdf"]
                    )
                    upload_btn = gr.Button(
                        "⚡ Process Document",
                        variant="primary"
                    )
                    upload_status = gr.Textbox(
                        label="Status",
                        lines=2,
                        interactive=False,
                        placeholder="Upload a PDF and click Process..."
                    )

                    gr.HTML("""
                    <div class="security-box">
                        <p style="color:#8b949e; font-size:12px; margin:0 0 8px 0; 
                        text-transform:uppercase; letter-spacing:1px;">
                        🛡️ Security Layers
                        </p>
                        <p class="security-item">✅ Prompt Injection Guard</p>
                        <p class="security-item">✅ Toxic Content Filter</p>
                        <p class="security-item">✅ Query Length Guard</p>
                        <p class="security-item">✅ Audit Logger Active</p>
                    </div>
                    """)

                with gr.Column(scale=2):
                    gr.Markdown("### 💬 Ask Questions")
                    query_input = gr.Textbox(
                        label="Your Question",
                        placeholder="e.g. What are the key skills? What is the main topic?",
                        lines=3
                    )
                    ask_btn = gr.Button(
                        "🔍 Get Answer",
                        variant="primary"
                    )
                    answer_output = gr.Textbox(
                        label="AI Answer",
                        lines=8,
                        interactive=False,
                        placeholder="Answer will appear here..."
                    )
                    sources_output = gr.Textbox(
                        label="📚 Sources Used From Document",
                        lines=6,
                        interactive=False,
                        placeholder="Source chunks will appear here..."
                    )

        with gr.Tab("📊 Audit Logs"):
            gr.Markdown("### 🔍 Query Audit Trail")
            gr.Markdown("Every query is logged with timestamp and security status.")
            refresh_btn = gr.Button("🔄 Refresh", variant="secondary")
            logs_output = gr.Textbox(
                label="Recent Queries",
                lines=15,
                interactive=False
            )
            refresh_btn.click(fn=get_logs, inputs=None, outputs=logs_output)

        with gr.Tab("ℹ️ Architecture"):
            gr.HTML("""
            <div class="arch-box">
                <h3 style="color:#e6edf3;">🏗️ System Architecture</h3>
                <pre style="color:#79c0ff;">
PDF Upload
    ↓ Text Extraction (pypdf)
    ↓ Chunk Splitting (300 word chunks)
    ↓ Sentence Embeddings (MiniLM)
    ↓ ChromaDB Vector Store
    
User Query
    ↓ Security Check Layer 1: Injection Detection
    ↓ Security Check Layer 2: Toxic Filter
    ↓ Security Check Layer 3: Length Guard
    ↓ Vector Similarity Search (Top 3 chunks)
    ↓ Claude AI (Grounded Answer)
    ↓ Audit Log (Timestamp + Status)
                </pre>
                <h3 style="color:#e6edf3;">🔧 Tech Stack</h3>
                <p>• <strong style="color:#79c0ff;">AI Model:</strong> Claude claude-sonnet-4-6 (Anthropic)</p>
                <p>• <strong style="color:#79c0ff;">Vector DB:</strong> ChromaDB + Sentence Transformers</p>
                <p>• <strong style="color:#79c0ff;">Embeddings:</strong> all-MiniLM-L6-v2 (local)</p>
                <p>• <strong style="color:#79c0ff;">Security:</strong> Custom 3-layer guardrails</p>
                <p>• <strong style="color:#79c0ff;">Logging:</strong> JSON audit trail</p>
                <p>• <strong style="color:#79c0ff;">UI:</strong> Gradio</p>
            </div>
            """)

    # ✅ Correct event connections
    upload_btn.click(
        fn=process_pdf,
        inputs=[pdf_input],
        outputs=[upload_status]
    )

    ask_btn.click(
        fn=answer_question,
        inputs=[query_input],
        outputs=[answer_output, sources_output]
    )

app.launch()