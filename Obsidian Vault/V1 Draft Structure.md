---

tags: [rag-project, structure, v1]

parent: [[RAG-Project-Learning-Notes]]

---

  

# V1 Draft Structure

  

Keep v1 deliberately small — get an end-to-end pipeline working before adding eval harness / visualizations.

  

```

rag-project/

├── data/

│   └── sample_docs/           # a small set of real documents (start with 3-5 files)

├── retrieval/

│   ├── chunking.py            # splits documents into chunks

│   ├── embeddings.py          # generates embeddings (sentence-transformers)

│   ├── similarity_numpy.py    # from-scratch cosine similarity search

│   └── vector_db.py           # ChromaDB/FAISS version (added after numpy version works)

├── backend/

│   ├── main.py                # FastAPI app, exposes /query endpoint

│   ├── llm_client.py          # wraps Groq/Gemini API calls

│   └── config.py              # API keys via .env, never hardcoded

├── frontend/

│   └── app.py                 # Streamlit app: chat box + retrieved chunks display

├── eval/                       # added in v2, not v1

├── requirements.txt

└── README.md

```

  

## V1 milestones (in order)

1. Load 3-5 sample documents, chunk them (fixed-size to start)

2. Generate embeddings for chunks using sentence-transformers

3. Implement cosine similarity in numpy, test retrieval manually with a few sample questions

4. Wrap retrieval in a FastAPI `/query` endpoint that also calls the LLM and returns an answer

5. Build a basic Streamlit chat UI that calls the `/query` endpoint and displays the answer + retrieved chunks

6. **Stop here for v1.** Get this working end-to-end before adding eval harness, embedding visualization, or swapping in a real vector DB — those come in v2.

  

## What's explicitly OUT of scope for v1

- Evaluation harness (precision/recall measurement)

- Embedding visualization (PCA/t-SNE)

- Swapping to ChromaDB/FAISS (stay with numpy version for v1)

- Any UI polish beyond a functional chat box

  

## Notes

- [ ] Confirm document set for v1

- [ ] Confirm chunk size chosen

- [ ] Date v1 was completed end-to-end