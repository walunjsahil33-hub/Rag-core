import numpy as np
def cosine_similarity(vector1, vector2):
    dot_product=np.dot(vector1,vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    if magnitude1==0 or magnitude2==0:
        return 0.0

    similarity=dot_product/(magnitude1*magnitude2)
    return float(similarity)


def find_similar_chunks(query_embedding,chunks_data,top_k=5)
    scored_chunks=[]

for chunk in chunks_data:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scored_chunks.append((chunk, score))

scored_chunks.sort(key=lambda item: item[1], reverse=True)
    
    return scored_chunks[:top_k]