================================================================
SECURERAG — ENTERPRISE AI DOCUMENT INTELLIGENCE SYSTEM
Complete Project Documentation
================================================================

WHAT IS THIS PROJECT?
----------------------------------------------------------------
SecureRAG is an AI-powered document question-answering system
with enterprise-grade security guardrails. You upload any PDF
document, ask questions about it, and the AI answers using ONLY
the content from that document — not from general knowledge.

The system also protects against malicious queries using 3
security layers and logs every interaction for compliance.


SIMPLE EXPLANATION (For Non-Technical People)
----------------------------------------------------------------
Think of it like this:
- You have a 100-page company report
- Instead of reading all 100 pages manually
- You upload it here and ask: "What was Q3 revenue?"
- The AI finds the exact section and answers instantly
- If someone tries to misuse the system, it gets blocked


HOW IT WORKS — STEP BY STEP
----------------------------------------------------------------

STEP 1: PDF UPLOAD
- User uploads any PDF file
- System accepts the file via Gradio UI
- File is passed to the processing pipeline

STEP 2: TEXT EXTRACTION
- Library Used: pypdf
- What it does: Opens the PDF and reads all text from every page
- Output: Raw text string from entire document
- Handles: Multi-page PDFs, different PDF formats

STEP 3: CHUNK SPLITTING
- Function: split_into_chunks()
- What it does: Breaks large text into smaller 300-word pieces
- Why: AI models work better with smaller focused chunks
- Example: 100-page PDF → 150 small chunks
- Output: List of text chunks

STEP 4: EMBEDDING GENERATION
- Model Used: all-MiniLM-L6-v2 (Sentence Transformers)
- What it does: Converts each text chunk into a number vector
- Why: Numbers can be mathematically compared for similarity
- Example: "revenue growth" → [0.23, 0.87, 0.45, ...]
- Runs: Completely FREE and locally on your computer
- Output: 384-dimensional vector for each chunk

STEP 5: VECTOR STORAGE
- Database Used: ChromaDB (free, local)
- What it does: Stores all chunk vectors in a searchable database
- Why: Enables fast similarity search later
- Output: Indexed vector database ready for search

STEP 6: USER ASKS QUESTION
- User types question in the UI text box
- Question is sent to the security check pipeline first

STEP 7: SECURITY CHECKS (3 Layers)
- File: security.py

  Layer 1 — Prompt Injection Detection:
  - Checks for phrases like "ignore previous instructions"
  - Checks for "act as", "pretend you are", "jailbreak"
  - Purpose: Prevents attackers from hijacking the AI
  - Result: Query blocked if injection detected

  Layer 2 — Toxic Content Filter:
  - Checks for harmful words like "hack", "exploit", "weapon"
  - Purpose: Prevents misuse of the system
  - Result: Query blocked if toxic content detected

  Layer 3 — Query Length Guard:
  - Checks if query exceeds 1000 characters
  - Purpose: Prevents token overflow attacks
  - Result: Query blocked if too long

STEP 8: AUDIT LOGGING
- File: logger.py
- What it does: Records every query with full details
- Logs: timestamp, query text, security result, blocked status
- Storage: audit_log.json file
- Purpose: Compliance, monitoring, traceability
- Example log entry:
  {
    "timestamp": "2026-06-22 10:30:00",
    "query": "What is the main topic?",
    "security_passed": true,
    "blocked": false
  }

STEP 9: VECTOR SIMILARITY SEARCH
- Function: retrieve_relevant_chunks()
- What it does: Converts user question to vector, then finds
  the 3 most similar chunks from the document
- How: Calculates cosine similarity between query vector
  and all stored chunk vectors
- Output: Top 3 most relevant text chunks from document

STEP 10: AI ANSWER GENERATION
- Model Used: Llama 3 8B via Groq API (FREE)
  OR Claude claude-sonnet-4-6 via Anthropic API
- Function: ask_claude()
- What it does: Sends the question + relevant chunks to AI
- Prompt structure: "Answer ONLY based on this context: [chunks]
  Question: [user query]"
- Constraint: AI cannot answer from general knowledge
- Output: Grounded answer based only on document content

STEP 11: DISPLAY ANSWER
- Answer shown in UI answer box
- If query was blocked: Shows security alert message
- If info not in document: Says "Information not found"


FILES IN THIS PROJECT
----------------------------------------------------------------

app.py
- Main application file
- Contains entire Gradio UI
- Connects all components together
- Handles button clicks and data flow
- 3 tabs: Document Q&A, Audit Logs, Architecture

rag_engine.py
- Core RAG logic
- Functions: extract_text_from_pdf, split_into_chunks,
  store_document, retrieve_relevant_chunks, ask_claude
- Manages ChromaDB connection
- Handles embedding generation

security.py
- All security guardrails
- Functions: check_prompt_injection, check_toxic_content,
  check_query_length, run_security_checks
- Returns: (is_safe: bool, message: string)

logger.py
- Audit logging system
- Functions: log_query, get_all_logs
- Reads/writes audit_log.json
- Stores complete query history

.env
- Stores API keys securely
- Never uploaded to GitHub
- Contains: ANTHROPIC_API_KEY, GROQ_API_KEY

requirements.txt
- All Python libraries needed
- Used for deployment


TECHNOLOGIES USED
----------------------------------------------------------------

PYTHON LIBRARIES:
- gradio          → Web UI framework
- pypdf           → PDF text extraction
- chromadb        → Vector database (local, free)
- sentence-transformers → Text embedding model
- groq            → Free LLM API client
- anthropic       → Claude API client
- python-dotenv   → Environment variable management

AI MODELS:
- all-MiniLM-L6-v2  → Embedding model (runs locally, free)
                       384-dimensional vectors
                       Converts text to numbers
- Llama 3 8B        → Answer generation (Groq, free)
                       8 billion parameter model
                       Understands and generates text
- Claude claude-sonnet-4-6  → Alternative answer model (Anthropic)

DATABASES:
- ChromaDB → Vector database
             Stores embeddings locally
             Fast similarity search
             No setup required, runs in memory

DEPLOYMENT:
- Hugging Face Spaces → Free cloud hosting
- GitHub → Code repository and version control


WHAT MAKES THIS PROJECT UNIQUE
----------------------------------------------------------------

1. SECURITY GUARDRAILS
   Most RAG projects have zero security.
   This has 3 layers of protection — same as enterprise systems.

2. AUDIT LOGGING
   Every query tracked with timestamp and security status.
   Shows compliance thinking — rare in student projects.

3. GROUNDED ANSWERS
   AI cannot hallucinate — answers only from document.
   Critical for real business use cases.

4. ARCHITECTURE TAB
   Shows system design thinking inside the app itself.
   Impresses technical interviewers.


RESUME DESCRIPTION
----------------------------------------------------------------

Project: SecureRAG — Enterprise AI Document Intelligence
- Built a production-grade RAG system enabling secure
  document Q&A with 3-layer security guardrails
- Implemented vector search using ChromaDB and
  Sentence Transformers for semantic similarity matching
- Integrated Llama 3 / Claude AI for grounded answer
  generation constrained to document context only
- Added prompt injection detection, toxic content
  filtering, and complete audit logging system
- Stack: Python, ChromaDB, Sentence Transformers,
  Groq/Llama3, Gradio, pypdf
- Live Demo: [HuggingFace Link]
- GitHub: [GitHub Link]


LINKEDIN POST TEMPLATE
----------------------------------------------------------------

🔒 Just built SecureRAG — an Enterprise AI Document Assistant!

Upload any PDF → Ask questions → Get AI answers instantly

What makes it production-ready:
✅ Vector search with ChromaDB
✅ Prompt injection detection
✅ Toxic content filtering
✅ Full audit trail logging
✅ Grounded answers (no hallucination)

Tech: Python | ChromaDB | Llama 3 | Sentence Transformers | Gradio

This is Week 1 of my 5-week AI Engineer project challenge.

#AI #MachineLearning #RAG #LLM #Python #AIEngineer

================================================================
END OF DOCUMENTATION
================================================================