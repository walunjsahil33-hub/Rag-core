---
tags: [rag-core, phase-1, person-4, backend]
parent: [[Phase 1 Overview]]
---

# Phase 1 — Role: Backend & Glue (Person 4)

## Your Mission

You are the orchestrator. You take everyone else's work and wire it into a working system.

**Core task:** Build a backend API that:
1. Receives a question from Person 3 (Streamlit frontend)
2. Calls Person 2's retrieval function to find relevant chunks
3. Sends those chunks + question to an LLM (Groq or Gemini)
4. Sends the answer back to Person 3

**You don't write the core logic** (Person 1 does embeddings, Person 2 does retrieval). **You orchestrate** — make them work together and expose it as an API.

---

## What you'll build (Concrete deliverable)

A FastAPI backend with one main endpoint:

```python
POST /query
Input: {"question": "What is machine learning?"}
Output: {
    "answer": "Machine learning is...",
    "retrieved_chunks": [
        {"chunk_id": "...", "text": "...", "similarity_score": 0.89},
        ...
    ]
}
```

That endpoint does:
1. Calls Person 2's `retrieve(question)` → gets chunks
2. Builds a prompt: question + chunks + instructions to LLM
3. Calls LLM API (Groq/Gemini) with that prompt
4. Returns answer + chunks used

---

## Code structure you'll create

```
project-root/
├── backend/
│   ├── main.py                 # FastAPI app, /query endpoint (YOUR CODE)
│   ├── llm_client.py          # Wraps LLM API calls (YOUR CODE)
│   ├── config.py              # API keys, settings (YOUR CODE)
│   └── requirements.txt        # Dependencies (YOUR CODE)
└── retrieval/
    ├── data_loader.py         # (Person 1's code — you'll import this)
    ├── embeddings.py          # (Person 1's code — you'll import this)
    ├── similarity_search.py   # (Person 2's code — you'll import this)
    └── retrieve.py            # (Person 2's code — you'll import this)
```

---

## Step-by-step what you'll code

### Step 1: Set up FastAPI

**File:** `backend/main.py`

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize the app
app = FastAPI(
    title="RAG Chatbot Backend",
    description="API for retrieving documents and generating answers"
)

# Define input/output models
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    retrieved_chunks: list

# Test endpoint to check if backend is running
@app.get("/ping")
def ping():
    return {"status": "ok"}

# The main endpoint (we'll build this next)
@app.post("/query")
def query(request: QueryRequest) -> QueryResponse:
    # We'll implement this in Step 3
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**What you need to understand:**
- `FastAPI` is a framework for building APIs
- `@app.post("/query")` creates an endpoint that accepts POST requests
- `BaseModel` defines the shape of input/output data
- `uvicorn` is the server that runs your FastAPI app

**Research:** "FastAPI tutorial for beginners" (20 min). Focus on:
- Creating endpoints
- Accepting JSON input
- Returning JSON output

---

### Step 2: Set up LLM client

**File:** `backend/llm_client.py`

```python
import os
from config import LLM_PROVIDER, LLM_API_KEY

def call_llm(prompt: str) -> str:
    """
    Send a prompt to an LLM and get the response.
    
    Input: prompt (string with question + context chunks)
    Output: answer from the LLM (string)
    """
    
    if LLM_PROVIDER == "groq":
        from groq import Groq
        
        client = Groq(api_key=LLM_API_KEY)
        
        message = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",  # Free Groq model
        )
        
        return message.choices[0].message.content
    
    elif LLM_PROVIDER == "gemini":
        import google.generativeai as genai
        
        genai.configure(api_key=LLM_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(prompt)
        return response.text
    
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")
```

**What you need to understand:**
- You're wrapping a third-party LLM API (Groq or Gemini)
- Input: a prompt (text). Output: generated text from the LLM
- Error handling: what if the API is down?

**Research:** 
- "Groq API tutorial" (10 min) OR "Google Gemini API tutorial" (10 min) — pick one
- Install their Python SDK: `pip install groq` or `pip install google-generativeai`
- Get a free API key (both offer generous free tiers)

---

### Step 3: Build the main `/query` endpoint

**File:** `backend/main.py`

```python
from retrieval.retrieve import retrieve  # Import Person 2's function
from llm_client import call_llm
import json

@app.post("/query")
def query(request: QueryRequest) -> QueryResponse:
    """
    Main endpoint: retrieve relevant chunks and generate answer
    """
    
    try:
        # Step 1: Load the embeddings data from Person 1
        with open("embeddings.json", "r") as f:
            chunks_data = json.load(f)
        
        # Step 2: Call Person 2's retrieval function
        retrieved_chunks = retrieve(
            query=request.question,
            chunks_data=chunks_data,
            top_k=5  # Return top 5 most relevant chunks
        )
        
        # Step 3: Build a prompt for the LLM
        context = "\n\n".join([
            f"[Chunk {i+1}] {chunk['text']}"
            for i, chunk in enumerate(retrieved_chunks)
        ])
        
        prompt = f"""You are a helpful assistant answering questions based on provided documents.

Use ONLY the following context to answer the question. If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {request.question}

Answer:"""
        
        # Step 4: Call the LLM
        answer = call_llm(prompt)
        
        # Step 5: Format and return response
        response = QueryResponse(
            answer=answer,
            retrieved_chunks=retrieved_chunks
        )
        
        return response
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="embeddings.json not found. Did Person 1 generate it?"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )
```

**What you need to understand:**
- Load Person 1's `embeddings.json`
- Call Person 2's `retrieve()` function with the question
- Build a prompt that includes both the question and the retrieved context
- Call the LLM with that prompt
- Return both the answer and the chunks (so Person 3 can show them)

**The prompt is crucial:** It tells the LLM "here's context, use ONLY this to answer". Without this instruction, the LLM might make things up (hallucinate).

---

### Step 4: Configuration & Environment variables

**File:** `backend/config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # or "gemini"
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

# Backend Configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY environment variable not set!")
```

**Create a `.env` file in the project root (never commit this to git):**

```
LLM_PROVIDER=groq
LLM_API_KEY=your_actual_groq_api_key_here
```

**What you need to understand:**
- Never hardcode API keys in code
- Use environment variables or `.env` files
- `.env` files should be in `.gitignore` (don't accidentally commit your API key to GitHub)

**Research:** "Python-dotenv tutorial" (5 min).

---

### Step 5: Dependencies & Installation

**File:** `backend/requirements.txt`

```
fastapi==0.104.0
uvicorn[standard]==0.24.0
pydantic==2.0.0
python-dotenv==1.0.0
groq==0.4.0          # If using Groq
# google-generativeai==0.3.0  # If using Gemini instead
requests==2.31.0
```

**Install them:**
```bash
pip install -r requirements.txt
```

---

## Running the backend

```bash
cd backend
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it (in a new terminal):**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'
```

---

## What you need to research (in priority order)

### Must-know (research these)
1. **FastAPI basics** — create endpoints, accept JSON input, return JSON — 20 min
2. **One LLM API** (Groq OR Gemini) — sign up, get API key, make first request — 20 min
3. **Environment variables in Python** — `.env` files, python-dotenv — 5 min
4. **Python error handling** — try/except blocks — 5 min

### Good-to-know
5. **CORS (Cross-Origin Resource Sharing)** — why does Person 3's frontend need special permission to call your backend? (10 min, optional but useful)
6. **Logging** — tracking what happens in your backend — 10 min (optional)

### Don't worry about
- Authentication/security (Phase 1 doesn't need it)
- Database design (you're using Person 1's JSON file)
- Deployment to cloud (Phase 1 is local)

---

## Testing your work (how to know you're done)

Before Phase 1 ends:

```
1. Does the backend start without errors?
   → command: python backend/main.py
   → Check: do you see "Uvicorn running"?

2. Does the /ping endpoint work?
   → Test: curl http://localhost:8000/ping
   → Check: do you get {"status": "ok"}?

3. Does /query endpoint work (with fake data)?
   → First, create a fake embeddings.json with a few test chunks
   → Test: curl with a test question
   → Check: does it return answer + chunks in correct format?

4. Can Person 3's frontend call it?
   → Have Person 3 test their Streamlit app pointing to your backend
   → Ask a question in the UI
   → Check: does the answer appear? Do the chunks show?

5. Does the answer make sense?
   → Look at the LLM output
   → Is it answering based on the retrieved context?
   → Or is it making things up (hallucinating)?
   → If hallucinating, try adjusting the prompt
```

**You're done when:** Frontend can call backend, backend retrieves chunks, LLM generates answers, everything works end-to-end.

---

## Common pitfalls to avoid

1. **Hardcoding API keys** — use `.env` files
2. **Not loading Person 1's embeddings.json** — make sure the file path is correct
3. **Not handling errors** — backend crashes = frontend gets no response. Use try/except.
4. **Wrong prompt format** — if LLM answers are bad, the problem is usually the prompt. Experiment.
5. **CORS errors** — if Person 3's frontend can't reach your backend, you might need to enable CORS:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Allow all origins for Phase 1 (not secure for production)
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

---

## What happens after you're done

Once your backend works:
- Person 3's frontend can call it
- Answers are generated and displayed
- Phase 1 is complete

You're the lynchpin of Phase 1 — if your backend doesn't work, nothing else matters. Test thoroughly.

---

## Questions to think about before you start

- [ ] Groq or Gemini? (Both are free, I'd suggest Groq for simplicity)
- [ ] Have I signed up for an API key?
- [ ] Have I tested the LLM API once locally before integrating into FastAPI?
- [ ] What if Person 1's embeddings.json takes a while? (Start with fake data)
