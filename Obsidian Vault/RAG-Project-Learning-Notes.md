---
tags: [project, rag, learning, team]
status: planning
version: v1-draft
---
  
  

# RAG Chatbot Project — Learning Notes & v1 Plan

  

> This is the **hub note** for our project. It gives a quick overview of what we're building and why, and links out to detailed notes for each part. Think of this page as the "table of contents" — click into a linked note whenever you want the full depth on that piece.

  

---

  

## What we're building (in plain terms)

  

We're building a chatbot that can answer questions using our *own* documents — not just what an LLM already knows. This is called **RAG (Retrieval-Augmented Generation)**.

  

In simple terms, the system does three things:

1. **Reads** a set of documents and breaks them into small pieces (chunks)

2. **Finds** the most relevant pieces for whatever question is asked

3. **Generates** an answer using an LLM, grounded in those relevant pieces

  

**Our twist:** instead of just importing libraries and calling it done, we build the core logic ourselves first (so we actually understand it), then upgrade to production tools, and add ways to measure whether our system is actually working well.

  

---

  

## Why we picked this project

  

Out of a list of ~25 beginner/intermediate project ideas, this one won because:

  

- **Teaches real math** — vectors, similarity, dimensionality reduction — most other ideas are mostly prompt engineering with little depth

- **Widely transferable** — retrieval and embeddings show up in almost every real AI product (search engines, support bots, even multi-agent systems)

- **Hard to fake** — we can *prove* our system works with real numbers (evaluation metrics), not just a demo that looks nice

- **Splits cleanly into 3 real roles** — everyone gets a meaty piece, not one person doing the "interesting part" while others do busywork

- **Free-tool friendly** — almost everything runs locally and free, so we're not blocked by API costs or rate limits

  

---

  

## The three components (click for full details)

  

| Component | What it does, briefly | Full notes |

|---|---|---|

| **Math & Retrieval Core** | Turns documents into chunks, converts them into numbers (embeddings), and finds the most relevant chunks for a question | [[Component 1 - Math & Retrieval Core]] |

| **Backend & Orchestration** | Connects everything — takes a question, calls retrieval, calls the LLM, sends back an answer | [[Component 2 - Backend & Orchestration]] |

| **Frontend & Visualization** | The chat interface users see, plus panels showing what got retrieved and why | [[Component 3 - Frontend & Visualization]] |

  

---

  

## Other key references

  

- **[[Shared Data Contract]]** — the exact "shape" of data each component will pass to the others. Agree on this *before* writing code — it's what keeps the three of you from stepping on each other.

- **[[V1 Draft Structure]]** — the actual folder structure and step-by-step build order for our first working version. Keep v1 small on purpose; fancier stuff comes later.

  

---

  

## How we're learning this (for complete beginners)

  

We are **not** going to sit down and deeply study every concept before writing code — that's a common beginner trap that kills momentum. Instead:

  

1. **Get a rough overview first** (just enough that the code doesn't feel like magic) — read through the linked component notes once, as a team, before splitting up

2. **Go deep only when you're actually building that part** — e.g., the person implementing similarity search is the one who should go read about cosine similarity in depth, right when they need it

3. **Use bugs as your study guide** — when something breaks, that's the most efficient signal for what to actually learn next, far better than guessing upfront what might matter

  

---

  

## Free tools we're using (so no one gets blocked by costs)

  

| Purpose | Tool | Why |

|---|---|---|

| Embeddings | `sentence-transformers` (local, no API key) | Free forever, no rate limits |

| Vector search (after our own version) | ChromaDB or FAISS | Free, open-source, local |

| LLM answers | Groq or Google Gemini (free tier) | Generous limits, no billing setup needed |

| Backend | FastAPI | Lightweight, good for learning API design |

| Frontend | Streamlit (or React if we want a resume-focused option) | Fast to build with as beginners |

  

---

  

## Open questions to settle as a team

- [ ] Which documents are we using for v1? (our own class notes vs. a real open-source project's docs)

- [ ] Streamlit or React for frontend?

- [ ] Groq or Gemini for the LLM step?

- [ ] Who owns which component?