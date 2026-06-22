import gradio as gr
import tempfile
import os
from rag_engine import extract_text_from_pdf, store_document, retrieve_relevant_chunks, ask_claude
from security import run_security_checks
from logger import log_query

def process_pdf(pdf_file):
    if pdf_file is None:
        return "⚠️ Please upload a PDF first"
    
    with open(pdf_file.name, 'rb') as f:
        text = extract_text_from_pdf(f)
    
    chunks = store_document(text, "document")
    return f"✅ Document processed! {chunks} chunks stored."

def answer_question(query):
    if not query:
        return "Please enter a question"
    
    # Security check
    is_safe, security_msg = run_security_checks(query)
    log_query(query, is_safe, security_msg)
    
    if not is_safe:
        return f"🚨 BLOCKED: {security_msg}"
    
    # Get answer
    chunks = retrieve_relevant_chunks(query)
    answer = ask_claude(query, chunks)
    return answer

# Build UI
with gr.Blocks(title="SecureRAG Assistant") as app:
    gr.Markdown("# 🔒 SecureRAG — AI Document Assistant")
    
    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
            upload_btn = gr.Button("Process Document", variant="primary")
            upload_status = gr.Textbox(label="Status")
        
        with gr.Column():
            query_input = gr.Textbox(label="Ask a Question")
            ask_btn = gr.Button("Ask", variant="primary")
            answer_output = gr.Textbox(label="Answer", lines=5)
    
    upload_btn.click(process_pdf, inputs=pdf_input, outputs=upload_status)
    ask_btn.click(answer_question, inputs=query_input, outputs=answer_output)

app.launch()