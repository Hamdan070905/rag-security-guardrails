import os
from anthropic import Anthropic
import chromadb
from sentence_transformers import SentenceTransformer
import pypdf
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
chroma_client = chromadb.Client()
embedder = SentenceTransformer('all-MiniLM-L6-v2')
collection = chroma_client.get_or_create_collection("documents")

def extract_text_from_pdf(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        if not text.strip():
            return None, "PDF appears to be image-based. Please use a text-based PDF."
        return text, None
    except Exception as e:
        return None, str(e)

def split_into_chunks(text, chunk_size=300):
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) < chunk_size:
            current += sentence + ". "
        else:
            if current.strip():
                chunks.append(current.strip())
            current = sentence + ". "
    if current.strip():
        chunks.append(current.strip())
    return chunks if chunks else [text[:500]]

def store_document(text, doc_name):
    try:
        # Clear old data
        try:
            chroma_client.delete_collection("documents")
        except:
            pass
        
        global collection
        collection = chroma_client.get_or_create_collection("documents")
        
        chunks = split_into_chunks(text)
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                embedding = embedder.encode(chunk).tolist()
                collection.add(
                    embeddings=[embedding],
                    documents=[chunk],
                    ids=[f"chunk_{i}"]
                )
        return len(chunks)
    except Exception as e:
        return 0

def retrieve_relevant_chunks(query, top_k=3):
    try:
        count = collection.count()
        if count == 0:
            return ["No document loaded."]
        query_embedding = embedder.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, count)
        )
        return results['documents'][0]
    except Exception as e:
        return [f"Retrieval error: {str(e)}"]

def ask_claude(query, context_chunks):
    try:
        from groq import Groq
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        context = "\n\n".join(context_chunks)
        
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",  # Free model
            messages=[
                {
                    "role": "user",
                    "content": f"""Answer based ONLY on this context:

Context:
{context}

Question: {query}

If answer not in context, say 'Information not found in document.'"""
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API Error: {str(e)}"