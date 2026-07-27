---
tags: [rag-core, phase-1, contract, interface]
parent: [[Phase 1 Overview]]
---

# Phase 1 — Data Contract (How Everything Connects)

## What is this?

This is the **interface agreement** between the four roles. It defines the exact format of data that each person will pass to the next.

**Why it matters:** If Person 1 outputs data in one format and Person 2 expects a different format, integration breaks. This contract prevents that.

**Rule:** Everyone must follow this contract exactly. If you need to change it, tell everyone first.

---

## Person 1 → Person 2: `embeddings.json`

**Person 1** outputs this file. **Person 2** loads and uses it.

**File format:** JSON array

**File path:** `embeddings.json` (in project root)

**Structure:**

```json
[
  {
    "chunk_id": "doc1_chunk0",
    "text": "This is the first chunk of text from the first document...",
    "source_doc": "document1.txt",
    "chunk_position": 0,
    "embedding": [0.123, -0.456, 0.789, ..., 0.234]
  },
  {
    "chunk_id": "doc1_chunk1",
    "text": "This is the second chunk from the first document...",
    "source_doc": "document1.txt",
    "chunk_position": 1,
    "embedding": [0.234, -0.567, 0.890, ..., 0.345]
  },
  {
    "chunk_id": "doc2_chunk0",
    "text": "First chunk from document 2...",
    "source_doc": "document2.txt",
    "chunk_position": 0,
    "embedding": [0.345, -0.678, 0.901, ..., 0.456]
  }
]
```

**Field breakdown:**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `chunk_id` | string | Yes | Unique identifier for this chunk (e.g., `doc1_chunk0`) |
| `text` | string | Yes | The actual text content of this chunk |
| `source_doc` | string | Yes | Which document this chunk came from (e.g., `document1.txt`) |
| `chunk_position` | int | Yes | Position in the document (chunk 0, chunk 1, etc.) |
| `embedding` | array of floats | Yes | The 384-number embedding for this chunk (from sentence-transformers) |

**Constraints:**
- Must have at least 10 chunks (more is better, 50+ is good for Phase 1)
- Each embedding must be exactly 384 numbers
- `chunk_id` must be unique (no duplicates)
- `text` must not be empty
- File must be valid JSON (use a JSON validator if unsure)

**Example (minimal, 2 chunks):**

```json
[
  {
    "chunk_id": "sample_chunk_0",
    "text": "Machine learning is a subset of artificial intelligence.",
    "source_doc": "sample.txt",
    "chunk_position": 0,
    "embedding": [0.1, 0.2, 0.3, ..., 0.384th_number]
  },
  {
    "chunk_id": "sample_chunk_1",
    "text": "It enables systems to learn from data without explicit programming.",
    "source_doc": "sample.txt",
    "chunk_position": 1,
    "embedding": [0.2, 0.3, 0.4, ..., 0.384th_number]
  }
]
```

---

## Person 2's `retrieve()` Function

**Person 2** implements this function. **Person 4** calls it.

**Function signature:**

```python
def retrieve(query: str, chunks_data: list, top_k: int = 5) -> list:
    """
    Find the most relevant chunks for a query.
    
    Args:
        query (str): User's question (e.g., "What is machine learning?")
        chunks_data (list): The list of chunks (loaded from embeddings.json)
        top_k (int): How many results to return (default 5)
    
    Returns:
        list: List of top-k chunks, sorted by relevance (highest first)
    """
```

**Return value format:**

```python
[
  {
    "chunk_id": "doc1_chunk3",
    "text": "The text of this chunk...",
    "source_doc": "document1.txt",
    "similarity_score": 0.87
  },
  {
    "chunk_id": "doc2_chunk1",
    "text": "Another chunk that was relevant...",
    "source_doc": "document2.txt",
    "similarity_score": 0.75
  },
  # ... up to 5 chunks, sorted by score (highest first)
]
```

**Constraints:**
- Must return exactly `top_k` chunks (or fewer if not enough chunks exist)
- Must be sorted by `similarity_score` in descending order (highest first)
- `similarity_score` must be a float between 0 and 1
- Each chunk must only include: `chunk_id`, `text`, `source_doc`, `similarity_score` (not the full embedding)

---

## Person 4's FastAPI Endpoint

**Person 4** implements this endpoint. **Person 3** (frontend) calls it.

### Request format:

**Endpoint:** `POST /query`

**Headers:** `Content-Type: application/json`

**Body:**

```json
{
  "question": "What is machine learning?"
}
```

### Response format:

**Status:** 200 OK (on success) or 500 (on error)

**Body:**

```json
{
  "answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed...",
  "retrieved_chunks": [
    {
      "chunk_id": "doc1_chunk0",
      "text": "The full text of the retrieved chunk...",
      "source_doc": "document1.txt",
      "similarity_score": 0.89
    },
    {
      "chunk_id": "doc2_chunk3",
      "text": "Another relevant chunk...",
      "source_doc": "document2.txt",
      "similarity_score": 0.76
    }
  ]
}
```

**Constraints:**
- `answer` must be a non-empty string (the LLM's response)
- `retrieved_chunks` must be a list (can be empty, but usually 5 items)
- Each chunk in the list must have: `chunk_id`, `text`, `source_doc`, `similarity_score`
- Response must be valid JSON

### Error response:

**Status:** 500 Internal Server Error

**Body:**

```json
{
  "detail": "Error message explaining what went wrong"
}
```

**Possible errors:**
- `"embeddings.json not found"` — Person 1 hasn't generated the file yet
- `"Could not connect to LLM API"` — API key is wrong or service is down
- `"Invalid question"` — question is empty

---

## Person 3's Frontend Integration

**Person 3** calls the Person 4's `/query` endpoint using Python's `requests` library:

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"question": user_input}
)

result = response.json()

# result now contains:
# result["answer"] → the LLM's answer
# result["retrieved_chunks"] → list of chunks with scores
```

---

## Visual flow of data

```
[Person 1]
documents.txt → chunking → embeddings.json
                                ↓
                         [Person 2]
                    embeddings.json → retrieve() function
                                        ↓
                                   [Person 4]
                         retrieve() → build prompt → LLM → /query endpoint
                                              ↑
                              Person 3 calls this endpoint
                                              ↓
                         /query returns: {answer, chunks}
                                              ↓
                           [Person 3]
                        displays answer + chunks in Streamlit
```

---

## Checklist before starting coding

- [ ] **Person 1:** Do you understand the embeddings.json format? Will you output exactly this structure?
- [ ] **Person 2:** Do you understand the retrieve() function signature? Will you return chunks in this exact format?
- [ ] **Person 3:** Do you understand the /query endpoint? Will you call it with {"question": "..."} ?
- [ ] **Person 4:** Do you understand the endpoint response format? Will you return {answer, retrieved_chunks}?
- [ ] **All:** If I need to change the contract, I'll tell everyone first (not just implement my own thing)?

---

## If you need to change the contract

**Don't silently change it.** Follow this process:

1. **Identify the problem** — "My use case needs an extra field"
2. **Propose the change to everyone** — "I think we should add X field because Y"
3. **Get agreement** — Everyone should be OK with it
4. **Update this note** — Write the change here so everyone sees it
5. **Update your code** — Now you can implement the change

**Example problem-solving conversation:**

- Person 2: "I need to return chunk embeddings too, not just text, so Person 3 can visualize them"
- Person 4: "That's fine, but will my backend have to pass those embeddings to Person 3?"
- Person 3: "Actually yes, I need them for the visualization. Let's add it."
- **Action:** Update contract to include `embedding` field in `/query` response

---

## Version history

| Date | Change | Reason |
|---|---|---|
| 2026-01-14 | Initial contract | Phase 1 kickoff |
| (updates as needed) | ... | ... |

