---
tags: [rag-core, phase-1, person-2, retrieval]
parent: [[Phase 1 Overview]]
---

# Phase 1 — Role: Retrieval Logic (Person 2)

## Your Mission

You are responsible for making search work. Given a user's question, your code finds the most relevant document chunks from Person 1's data.

**Core task:** Take a question → find the 5 most similar chunks → return them with similarity scores.

This is the **retrieval** in RAG. Everything else hangs on this working well.

---

## What you'll build (Concrete deliverable)

A Python module with one main function:

```python
def retrieve(query: str, chunks_data: list, top_k: int = 5) -> list:
    """
    Find the most relevant chunks for a query.
    
    Input:
      - query: user's question as a string (e.g., "What is machine learning?")
      - chunks_data: the JSON data Person 1 created (list of chunks with embeddings)
      - top_k: how many chunks to return (default 5)
    
    Output: list of top-k chunks, sorted by relevance (most relevant first)
    Example output:
    [
      {"chunk_id": "doc1_chunk3", "text": "...", "similarity_score": 0.87},
      {"chunk_id": "doc2_chunk1", "text": "...", "similarity_score": 0.75},
      ...
    ]
    """
```

**This one function is what Person 4 calls from the backend.**

---

## Code structure you'll create

```
project-root/
└── retrieval/
    ├── data_loader.py           # (Person 1's code — you'll use this)
    ├── embeddings.py            # (Person 1's code — you'll use this)
    ├── similarity_search.py     # YOUR CODE: the core retrieval logic
    └── retrieve.py              # YOUR CODE: wrapper function that ties it together
```

---

## Step-by-step what you'll code

### Step 1: Load Person 1's data

**File:** `retrieval/retrieve.py`

```python
import json
from embeddings import generate_embeddings

def load_embeddings(json_file_path):
    """
    Load the embeddings.json file that Person 1 created.
    
    Input: path to embeddings.json (e.g., "embeddings.json")
    Output: list of chunk objects with their embeddings
    """
    # pseudocode:
    # open the JSON file
    # parse it as JSON
    # return the list of chunks
```

**What you need to understand:** How to load a JSON file in Python.

**Research:** Search "Python load JSON file" — literally 3 lines of code.

---

### Step 2: Understand cosine similarity (the core concept)

**This is the math part. Don't be intimidated.**

Cosine similarity answers: "How similar are two lists of numbers?"

**Example:**
```
Vector A (embedding of "machine learning"): [0.1, 0.5, -0.3, 0.2, ...]
Vector B (embedding of "ML algorithms"):    [0.12, 0.48, -0.28, 0.19, ...]
Vector C (embedding of "cooking recipes"):  [0.8, -0.4, 0.1, 0.6, ...]

Cosine similarity(A, B) = 0.98  ← very similar, close to 1.0
Cosine similarity(A, C) = 0.15  ← very different, close to 0
```

**The formula:**

```
cosine_similarity(v1, v2) = (v1 · v2) / (||v1|| × ||v2||)

Where:
  v1 · v2  = dot product = sum of (v1[i] * v2[i])
  ||v1||   = magnitude = sqrt(sum of v1[i]²)
  ||v2||   = magnitude = sqrt(sum of v2[i]²)
```

**In plain English:** Take two vectors, multiply them element-wise, sum those products, divide by their magnitudes. Result is between -1 and 1 (closer to 1 = more similar).

**You don't need to derive it.** Just use the formula or use a library (numpy has it built-in).

---

### Step 3: Implement cosine similarity

**File:** `retrieval/similarity_search.py`

**Option A: Use numpy (recommended for learning)**

```python
import numpy as np

def cosine_similarity(vector1, vector2):
    """
    Calculate cosine similarity between two vectors.
    
    Input: two lists/arrays of numbers (embeddings)
    Output: similarity score between -1 and 1 (closer to 1 = more similar)
    """
    # pseudocode:
    # dot product: sum(v1[i] * v2[i])
    dot_product = np.dot(vector1, vector2)
    
    # magnitudes: sqrt(sum(v1[i]²))
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    
    # cosine similarity
    if magnitude1 == 0 or magnitude2 == 0:
        return 0  # avoid division by zero
    
    similarity = dot_product / (magnitude1 * magnitude2)
    return similarity
```

**Option B: Use scikit-learn (simpler)**

```python
from sklearn.metrics.pairwise import cosine_similarity

similarity_score = cosine_similarity([vector1], [vector2])[0][0]
```

**Recommendation:** Start with Option A (numpy). It teaches you the concept. Option B is faster but hides the math.

**What you need to understand:** The formula above. That's it. Don't go deep into linear algebra.

**Research:** Search "cosine similarity explained simply" (10 min video or blog post). You'll see the formula, maybe a geometric intuition (angle between vectors), and that's all you need.

---

### Step 4: Find similar chunks

**File:** `retrieval/similarity_search.py`

```python
def find_similar_chunks(query_embedding, all_chunk_embeddings, top_k=5):
    """
    Compare query embedding to all chunk embeddings, find top-k matches.
    
    Input:
      - query_embedding: the query converted to embedding (384 numbers)
      - all_chunk_embeddings: list of all chunks with their embeddings
      - top_k: how many to return
    
    Output: list of top-k chunks with their similarity scores
    """
    # pseudocode:
    # 1. for each chunk in all_chunk_embeddings:
    #      score = cosine_similarity(query_embedding, chunk.embedding)
    #      save (chunk, score)
    # 2. sort by score (highest first)
    # 3. return top k
```

**Example algorithm:**
```python
scores = []
for chunk in all_chunks:
    score = cosine_similarity(query_embedding, chunk["embedding"])
    scores.append((chunk, score))

# Sort by score, highest first
scores.sort(key=lambda x: x[1], reverse=True)

# Return top k
top_k_chunks = scores[:top_k]
return top_k_chunks
```

---

### Step 5: Tie it together (the main `retrieve` function)

**File:** `retrieval/retrieve.py`

```python
def retrieve(query, chunks_data, top_k=5):
    """
    Complete retrieval pipeline:
    query → embed → find similar → return top chunks
    """
    # 1. Load embeddings.json (or chunks_data is passed in)
    # 2. Embed the query (use Person 1's embeddings module)
    query_embedding = generate_embeddings([query])[0]
    
    # 3. Find similar chunks
    top_chunks = find_similar_chunks(query_embedding, chunks_data, top_k)
    
    # 4. Format output
    result = []
    for chunk, score in top_chunks:
        result.append({
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "source_doc": chunk["source_doc"],
            "similarity_score": float(score)  # convert to float for JSON
        })
    
    return result
```

---

## What you need to research (in priority order)

### Must-know (research these)
1. **How to load JSON in Python** — 5 min
2. **Numpy basics** — arrays, `np.dot()`, `np.linalg.norm()` — 20 min
3. **Cosine similarity formula** — 15 min (search "cosine similarity explained")
4. **Sorting lists in Python** — `.sort()` method — 5 min

### Good-to-know
5. **Linear algebra intuition** — what does a vector mean geometrically? (30 min optional, helps understanding)
6. **Why cosine similarity over other metrics** — why not Euclidean distance? (optional read)

### Don't worry about
- Implementing cosine similarity from pure math (use numpy)
- Optimization tricks (we'll do that in Phase 2)

---

## Testing your work (how to know you're done)

Before you hand off to Person 4, check these:

```python
# 1. Can I load embeddings.json?
#    → embeddings = load_embeddings("embeddings.json")
#    → Check: is it a list? Does each item have "text" and "embedding"?

# 2. Can I compute cosine similarity?
#    → pick two embeddings from the data
#    → score = cosine_similarity(emb1, emb2)
#    → Check: is score between -1 and 1? Is similar text scoring ~0.8+?

# 3. Can I find similar chunks?
#    → query = "What is the main topic?"
#    → results = retrieve(query, embeddings_data, top_k=5)
#    → Check: did it return 5 chunks? Are they sorted by similarity score?

# 4. Manual sanity check
#    → Look at the top result text — does it actually seem relevant to the query?
#    → Does the similarity score make sense? (high = relevant, low = not)
```

**You're done when:** `retrieve()` function works end-to-end and returns relevant chunks for test queries.

---

## Common pitfalls to avoid

1. **Forgetting to normalize vectors** — magnitudes matter for cosine similarity. Use `np.linalg.norm()`.
2. **Returning chunks in wrong order** — sort by score, highest first (that's most relevant).
3. **Not handling the query embedding correctly** — remember, the query is just text too, needs to be embedded first.
4. **Returning wrong format** — make sure output matches what Person 4 expects (see [[Phase 1 - Data Contract]]).

---

## What happens after you're done

Once `retrieve()` works:
- **Person 4** calls it from the backend
- Person 4 passes the top chunks to an LLM: "Here's context, answer the question"
- Person 3 displays the answer to users

If retrieval is bad, answers are bad. So test thoroughly.

---

## Questions to think about before you start

- [ ] Will I use numpy or scikit-learn for cosine similarity?
- [ ] How will I test my retrieve() function? (create a few test queries first)
- [ ] Should I handle edge cases like empty queries? (optional for Phase 1, but good to think about)
