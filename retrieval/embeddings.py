from sentence_transformers import SentenceTransformer

def generate_embeddings(chunks):
    """Convert text chunks into 384-dimensional embedding vectors."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks, convert_to_tensor=False)
    return embeddings.tolist()