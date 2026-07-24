---

tags: [rag-project, structure, v1]

parent: [[RAG-Project-Learning-Notes]]

---
---

tags: [rag-project, contract, integration]

parent: [[RAG-Project-Learning-Notes]]

---

  

# Shared Data Contract

  

**Agree on this BEFORE writing code** — avoids painful integration issues later, since all three components need to speak the same "shape" of data.

  

```

A "chunk" looks like:

{

  "chunk_id": string,

  "text": string,

  "source_doc": string,

  "embedding": list[float]   // added after embedding step

}

  

A "query request" (frontend → backend) looks like:

{

  "question": string

}

  

A "query response" (backend → frontend) looks like:

{

  "answer": string,

  "retrieved_chunks": [

    { "chunk_id": string, "text": string, "similarity_score": float }

  ]

}

```

  

## Why this matters

- The retrieval person (Component 1) needs to know exactly what shape of object to hand off to the backend

- The backend person (Component 2) needs to know exactly what the frontend expects back

- The frontend person (Component 3) can literally start building their UI against this *fake* data before the backend is even done — unblocks the whole team from waiting on each other

  

## Rule of thumb

If you want to change this contract mid-project (e.g., add a new field), post it to the team first — a silent change here is the #1 cause of "why isn't this working" bugs between components.

  ## Ownership note
Roles rotate across phases — everyone works on retrieval, backend, and frontend 
at some point. This contract defines the interface between components, not 
permanent ownership. Whoever is working on a given component at a given time 
must follow this contract so the other parts don't break.

## Notes

- [ ] Did we change this contract at all during the build? Document what and why.