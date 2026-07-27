---
tags: [rag-core, phase-1, overview]
status: planning
---

# Phase 1 Overview — Building a Basic RAG Pipeline

## What is Phase 1?

Phase 1 is our **first working end-to-end RAG system**. We're building the simplest possible version that actually works — not polished, not optimized, just *functional*.

By the end of Phase 1, you should be able to:
1. Ask the system a question
2. It retrieves relevant documents
3. It generates an answer using those documents
4. You see the answer in a chat interface

That's it. Everything else (embeddings optimization, evaluation metrics, visualization) comes later.

---

## How the pipeline flows

```
[User asks a question in Streamlit]
            ↓
[Backend receives question via API]
            ↓
[Retrieval finds relevant document chunks]
            ↓
[LLM generates answer from those chunks]
            ↓
[Answer shown back in Streamlit]
```

Each person owns one piece, but they all connect in sequence.

---

## The 4 roles (and why they're separate)

| Role | Owner | Why this makes sense |
|---|---|---|
| **Data & Embeddings** | Person 1 | Someone has to prepare the data first. No retrieval without documents. |
| **Retrieval Logic** | Person 2 | Once data is ready, finding relevant chunks is a distinct problem — doesn't require backend knowledge. |
| **Frontend** | Person 3 | UX is separate — can be built in parallel, doesn't depend on backend being done. |
| **Backend & Glue** | Person 4 | Takes everyone else's work and wires it together into working endpoints. Orchestration owner. |

**Key insight:** Roles are divided by *responsibility*, not by skill. Each person understands the full pipeline, but owns one critical piece.

---

## Timeline & Dependencies

```
Week 1:
  - Person 1 starts: documents → chunks → embeddings (JSON file)
  - Person 3 starts: simple Streamlit chat UI (hardcoded answer for now)
  - Person 2 & 4: ready to start once Person 1's JSON file is available

Week 2:
  - Person 2: builds retrieval logic (uses Person 1's JSON)
  - Person 4: builds backend (uses Person 2's retrieval function, calls LLM)
  - Person 3: connects Streamlit to Person 4's backend API

Week 3:
  - All test together, fix bugs, ship Phase 1
```

**Not strictly sequential** — Person 3 and 1 can work in parallel. Person 2 and 4 start once Person 1 is done (can be overlapping).

---

## Technology stack (Phase 1 only)

| Component | Tool | Why |
|---|---|---|
| Language | Python 3.9+ | Everyone should have it, or install via conda/pip |
| Documents | `.txt` files in `/data` folder | Simplest to start. PDFs/CSVs come later. |
| Embeddings model | `sentence-transformers` (all-MiniLM-L6-v2) | Free, runs locally, no API key, fast |
| Similarity search | numpy (cosine similarity) | You'll write the math yourself first, understand it deeply |
| LLM | Groq or Google Gemini (free tier) | One free API call per query — no cost bloat |
| Backend | FastAPI | Lightweight, easy to learn, used in real production systems |
| Frontend | Streamlit | Build interactive apps in 50 lines of Python, no HTML/CSS needed |
| Data format | JSON | Human-readable, easy to debug, no database setup needed |

---

## Shared understanding before anyone codes

**Everyone should read and understand:**
1. What is an embedding? (rough explanation: text → numbers that capture meaning)
2. What is cosine similarity? (rough explanation: comparing how similar two numbers-lists are)
3. What is an API? (rough explanation: a way to call code from another program)
4. What is an LLM? (you know this: a model that generates text)

**Depth needed:** Surface level. Don't go study linear algebra or deep neural networks. Just enough to not feel lost reading your teammate's code.

---

## Success criteria for Phase 1

Phase 1 is **done** when:
- [ ] Person 1's embeddings JSON file exists and can be loaded by Person 2
- [ ] Person 2's retrieval function returns relevant chunks for test queries
- [ ] Person 4's `/query` endpoint returns an actual answer from the LLM
- [ ] Person 3's Streamlit app calls that endpoint and displays the answer
- [ ] All 4 of you can ask a question and get an answer back (even if it's sometimes wrong)
- [ ] You can explain to each other what each role does without looking at notes

**What's NOT in Phase 1:** evaluation, optimization, visualization, hybrid retrieval, fancy UI. Keep scope tight.

---

## What each role owns (one-line summary)

- **Person 1:** Prepare data so the system can search it
- **Person 2:** Make searching actually work
- **Person 3:** Make it pretty and interactive (for users)
- **Person 4:** Wire 1+2+3 together and make it handle requests

---

## Open questions to settle as a team

- [ ] Which documents are we using? (class notes, a real open-source project, something else?)
- [ ] Groq or Gemini for the LLM?
- [ ] How many documents to start with? (aim for 3-5 to keep v1 small)
- [ ] Who's responsible for Git? (pushing code, managing branches, code review)
