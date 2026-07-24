---

tags: [rag-project, component, retrieval]

parent: [[RAG-Project-Learning-Notes]]

---

  

# Component 1 — Math & Retrieval Core

  

**What this part does:** takes documents → breaks them into chunks → converts chunks into numbers (embeddings) → finds the most relevant chunks for a given question.

  

## Concepts to research before starting

- **What is an embedding?** A way to represent text as a list of numbers/vector, such that similar meanings → similar numbers.

- **Cosine similarity** — the math formula used to measure how "close" two vectors are. This is the heart of retrieval. Output ranges from -1 to 1; closer to 1 means more similar.

- **Chunking strategies** — why we can't just feed a whole document to the model at once (context limits, relevance dilution). Research: fixed-size chunking vs. sentence-based chunking vs. overlapping chunks.

- **What a vector database is and why we'd eventually want one** — fast similarity search at scale. We build the naive version ourselves first in numpy to understand it, then swap in a real one.

  

## Frameworks/tools to look into

- **numpy** — for building cosine similarity from scratch (this comes first, before any library)

- **sentence-transformers** — open-source, local embedding model (no API key needed). Look up the `all-MiniLM-L6-v2` model specifically.

- **ChromaDB** or **FAISS** — vector databases we'll swap in *after* the from-scratch version works

  

## Beginner-friendly resources to look up

- Search: "cosine similarity explained simply"

- Search: "sentence-transformers quickstart"

  

## Build order (do this, don't skip ahead)

1. Load a few sample documents

2. Chunk them (fixed-size to start — simplest to implement)

3. Generate embeddings for each chunk using sentence-transformers

4. Write cosine similarity from scratch in numpy — test it manually against a few sample questions

5. Only after that works: swap in ChromaDB/FAISS and compare speed/results

  

## Notes / questions to fill in as we build

- [ ] Which chunk size did we start with, and why?

- [ ] What did we notice when comparing chunking strategies?

- [ ] Any surprises in retrieval quality?