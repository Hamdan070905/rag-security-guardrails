import streamlit as st
import tempfile
import os
from rag_engine import extract_text_from_pdf, store_document, retrieve_relevant_chunks, ask_claude
from security import run_security_checks

# Page config
st.set_page_config(
    page_title="SecureRAG Assistant",
    page_icon="🔒",
    layout="wide"
)

# Title
st.title("🔒 SecureRAG — AI Document Assistant")
st.caption("Upload any PDF and ask questions securely")

# Sidebar
with st.sidebar:
    st.header("📁 Upload Document")
    uploaded_file = st.file_uploader("Choose PDF", type="pdf")
    
    if uploaded_file:
        with st.spinner("Processing document..."):
            # Save temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            # Extract and store
            with open(tmp_path, 'rb') as f:
                text = extract_text_from_pdf(f)
            
            chunks_count = store_document(text, uploaded_file.name)
            os.unlink(tmp_path)
            
        st.success(f"✅ Document processed!")
        st.info(f"📊 {chunks_count} chunks stored")
        st.session_state['doc_loaded'] = True
        st.session_state['doc_name'] = uploaded_file.name

    # Security Status Panel
    st.divider()
    st.header("🛡️ Security Status")
    st.success("✅ Injection Detection: ON")
    st.success("✅ Toxic Filter: ON")
    st.success("✅ Length Guard: ON")

# Main chat area
st.header("💬 Ask Questions")

# Chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

# Query input
query = st.chat_input("Ask anything about your document...")

if query:
    # Show user message
    with st.chat_message("user"):
        st.write(query)
    
    # Run security check FIRST
    is_safe, security_msg = run_security_checks(query)
    
    if not is_safe:
        # Block unsafe query
        with st.chat_message("assistant"):
            st.error(security_msg)
            st.warning("Your query was blocked by security guardrails.")
        
        st.session_state.messages.append({
            'role': 'assistant',
            'content': f"BLOCKED: {security_msg}"
        })
    
    elif not st.session_state.get('doc_loaded'):
        with st.chat_message("assistant"):
            st.warning("⚠️ Please upload a PDF document first!")
    
    else:
        # Safe query — get answer
        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                
                # Retrieve relevant chunks
                chunks = retrieve_relevant_chunks(query)
                
                # Get Claude answer
                answer = ask_claude(query, chunks)
                
                # Show answer
                st.write(answer)
                
                # Show sources (unique feature!)
                with st.expander("📚 View Source Chunks Used"):
                    for i, chunk in enumerate(chunks):
                        st.text_area(f"Source {i+1}", chunk, height=100)
        
        # Save to history
        st.session_state.messages.append({'role': 'user', 'content': query})
        st.session_state.messages.append({'role': 'assistant', 'content': answer})