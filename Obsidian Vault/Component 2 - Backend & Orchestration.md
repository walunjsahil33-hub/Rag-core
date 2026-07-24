---
tags: [rag-project, component, backend]
parent: [[RAG-Project-Learning-Notes]]
---

# Component 2 — Backend & Orchestration

**What this part does:** the "glue" — takes a user's question from the frontend, calls the retrieval logic, sends the retrieved chunks + question to an LLM, and returns the answer.

## Concepts to research before starting
- **What an API is** and how a frontend talks to a backend (request → response)
- **What "orchestration" means here** — the backend doesn't do the thinking itself, it coordinates: retrieval step → LLM call step → response formatting
- **Prompt construction** — how to combine a user's question + retrieved chunks into a single prompt sent to the LLM
- **Rate limits & token usage** — since we're using free-tier APIs, understanding what "tokens" are and why logging usage matters

## Frameworks/tools to look into
- **FastAPI** — lightweight Python framework for building the API
- **Groq API** or **Google Gemini API** — free-tier LLM providers
- **python-dotenv** — for managing API keys safely (never hardcode keys in code)

## Beginner-friendly resources to look up
- Search: "FastAPI hello world tutorial"
- Search: "Groq API quickstart" or "Gemini API quickstart"

## Build order
1. Get a basic FastAPI app running with a single test endpoint (e.g., `/ping`)
2. Set up `.env` file for API keys, load with python-dotenv
3. Write a simple function that calls Groq/Gemini with a hardcoded prompt, confirm it works
4. Build the real `/query` endpoint: takes a question → calls retrieval (Component 1) → builds prompt with retrieved chunks → calls LLM → returns answer + chunks used
5. Add basic logging (what was retrieved, how many tokens used, response time)

## Notes / questions to fill in as we build
- [ ] Which LLM provider did we settle on, and why?
- [ ] What did our final prompt template look like?
- [ ] Any rate limit issues encountered?
