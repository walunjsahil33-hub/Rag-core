---

tags: [rag-project, component, frontend]

parent: [[RAG-Project-Learning-Notes]]

---

  

# Component 3 — Frontend & Visualization

  

**What this part does:** the interface users interact with — chat window, plus "transparency" panels showing which chunks were retrieved, their similarity scores, and (later) evaluation results.

  

## Concepts to research before starting

- **Basic React or Streamlit fundamentals** (pick one — Streamlit is faster for beginners, React is more resume-relevant if you already have some frontend comfort)

- **What dimensionality reduction is** (PCA or t-SNE) — a way to squish high-dimensional embeddings down to 2D so we can plot and *see* clusters of similar content

- **How to call a backend API from a frontend** (fetch requests / axios if React, or `requests` if Streamlit)

  

## Frameworks/tools to look into

- **Streamlit** (recommended for v1 — much faster to build with as a beginner) or **React** (if more resume-focused)

- **matplotlib** or **plotly** — for the embedding visualization panel

- **scikit-learn** — has built-in PCA/t-SNE functions, no need to implement from scratch

  

## Beginner-friendly resources to look up

- Search: "Streamlit tutorial for beginners"

- Search: "PCA visualization explained simply"

  

## Build order

1. Basic Streamlit app: a text input box + a "submit" button

2. Wire it up to call the backend `/query` endpoint, display the raw answer

3. Add a panel showing retrieved chunks + their similarity scores next to the answer

4. (v2, not v1) Add embedding visualization panel using PCA/t-SNE

5. (v2, not v1) Add eval metrics dashboard

  

## Notes / questions to fill in as we build

- [ ] Streamlit or React — which did we pick, and why?

- [ ] What does the chunk transparency panel look like?

- [ ] Any UI decisions worth documenting?