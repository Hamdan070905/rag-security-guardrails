import os
from anthropic import Anthropic
import chromadb
from sentence_transformers import SentenceTransformer
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

# Initialize everything
client = Anthropic()
chroma_client = chromadb.Client()
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Free, runs locally

# Create vector collection
collection = chroma_client.get_or_create_collection("documents")

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def split_into_chunks(text, chunk_size=500):
    """Split text into smaller chunks"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        current_chunk.append(word)
        current_size += 1
        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def store_document(text, doc_name):
    """Generate embeddings and store in ChromaDB"""
    chunks = split_into_chunks(text)
    
    for i, chunk in enumerate(chunks):
        embedding = embedder.encode(chunk).tolist()
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[f"{doc_name}_chunk_{i}"]
        )
    return len(chunks)

def retrieve_relevant_chunks(query, top_k=3):
    """Find most relevant chunks for query"""
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0]

def ask_claude(query, context_chunks):
    """Send context + query to Claude"""
    context = "\n\n".join(context_chunks)
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""Answer based ONLY on this context:

Context:
{context}

Question: {query}

If answer not in context, say 'Information not found in documents.'"""
            }
        ]
    )
    return response.content[0].text