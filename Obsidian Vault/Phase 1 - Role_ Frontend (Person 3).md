---
tags: [rag-core, phase-1, person-3, frontend]
parent: [[Phase 1 Overview]]
---

# Phase 1 — Role: Frontend (Person 3)

## Your Mission

You are responsible for the user experience. You build the interface where users ask questions and see answers.

**Core task:** Create a chat application in Streamlit that:
1. Takes user input (text box)
2. Sends it to Person 4's backend API
3. Receives an answer
4. Displays it nicely (plus the chunks that were retrieved)

**You own the entire user-facing layer.** Your work is independent of the retrieval/backend complexity — if the API works, your UI will work.

---

## What you'll build (Concrete deliverable)

A Streamlit app (`frontend/app.py`) that:
- Looks like a chat interface
- Has a text input where users ask questions
- Calls Person 4's API endpoint when user submits
- Shows the answer + the document chunks that were used

**Example flow:**
```
User types: "What is machine learning?"
        ↓
[Submit button clicked]
        ↓
Frontend sends question to backend API
        ↓
Backend returns: {answer: "...", retrieved_chunks: [...]}
        ↓
Frontend displays answer + chunks in a nice format
```

---

## Code structure you'll create

```
project-root/
└── frontend/
    ├── app.py                   # Main Streamlit app (YOUR CODE)
    └── config.py                # Configuration (backend URL, etc.) (YOUR CODE)
```

**That's it.** Streamlit does a lot for you, so you don't need 10 files.

---

## Step-by-step what you'll code

### Step 1: Set up Streamlit

**File:** `frontend/app.py`

```python
import streamlit as st
import requests
from config import BACKEND_URL

# Set page title and layout
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("📚 Document Q&A Chatbot")
st.write("Ask questions about our documents and get answers!")

# Your code goes here
```

**What you need to understand:** Streamlit is a framework that turns Python scripts into interactive web apps with minimal code. No HTML, no CSS, just Python.

**Research:** Search "Streamlit tutorial for beginners" (15 min). Watch their quickstart video or read their getting started guide.

---

### Step 2: Build the chat input

**File:** `frontend/app.py`

```python
# Input section
st.subheader("Ask a question:")
user_question = st.text_input("Your question:", placeholder="e.g., What is machine learning?")

if st.button("Search"):
    if user_question.strip():  # Make sure question is not empty
        # We'll fill this in Step 3
        pass
    else:
        st.warning("Please enter a question!")
```

**What you need to understand:**
- `st.text_input()` creates a text box
- `st.button()` creates a clickable button
- `if st.button("Search"):` runs code when user clicks

**Research:** Streamlit input widgets documentation (10 min).

---

### Step 3: Call the backend API

**File:** `frontend/app.py`

```python
import streamlit as st
import requests
from config import BACKEND_URL

def query_backend(question):
    """
    Send a question to Person 4's backend API, get answer + chunks.
    
    Input: user's question (string)
    Output: {answer: "...", retrieved_chunks: [...]}
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/query",  # Person 4's endpoint
            json={"question": question},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()  # {answer: "...", retrieved_chunks: [...]}
        else:
            return {"error": f"Backend error: {response.status_code}"}
    
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to backend. Is it running?"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


# In your main code:
if st.button("Search"):
    if user_question.strip():
        st.write("Searching...")  # Show loading message
        result = query_backend(user_question)
        
        if "error" in result:
            st.error(result["error"])
        else:
            # We'll display results in Step 4
            pass
```

**What you need to understand:** 
- `requests.post()` sends a request to an API endpoint
- API expects JSON input: `{"question": "..."}`
- API returns JSON: `{"answer": "...", "retrieved_chunks": [...]}`
- Error handling: what if backend is down?

**Research:** "Python requests library tutorial" (10 min).

---

### Step 4: Display the results

**File:** `frontend/app.py`

```python
# After getting result from backend:
if "error" not in result:
    # Show the answer
    st.subheader("Answer:")
    st.write(result["answer"])
    
    # Show retrieved chunks
    st.subheader("📄 Retrieved Documents:")
    
    chunks = result.get("retrieved_chunks", [])
    
    for i, chunk in enumerate(chunks, 1):
        with st.expander(f"Chunk {i} (Similarity: {chunk.get('similarity_score', 'N/A'):.2f})"):
            st.write(f"**Source:** {chunk.get('source_doc', 'Unknown')}")
            st.write(f"**Text:** {chunk.get('text', 'N/A')}")
```

**What you need to understand:**
- `st.subheader()` creates a subheading
- `st.write()` displays text
- `st.expander()` creates a collapsible section (click to expand/collapse)
- `chunk.get('key', 'default')` safely gets a value from a dictionary

**Research:** Streamlit display elements (10 min).

---

### Step 5: Add configuration

**File:** `frontend/config.py`

```python
# Backend configuration
BACKEND_URL = "http://localhost:8000"  # Person 4's FastAPI will run on this

# UI configuration (optional)
APP_TITLE = "📚 Document Q&A Chatbot"
PLACEHOLDER_QUESTION = "e.g., What is machine learning?"
```

**Why:** This way, if Person 4 changes the backend URL, you just update this one file.

---

### Step 6 (Optional): Add chat history

**For Phase 1, this is optional. Add if you want the app to feel more like a real chatbot.**

```python
# At the top of app.py, after streamlit setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# After getting a result:
if "error" not in result:
    st.session_state.chat_history.append({
        "question": user_question,
        "answer": result["answer"]
    })

# Display chat history at bottom
if st.session_state.chat_history:
    st.subheader("Chat History:")
    for item in st.session_state.chat_history:
        st.write(f"**Q:** {item['question']}")
        st.write(f"**A:** {item['answer']}")
        st.write("---")
```

**What you need to understand:** `st.session_state` stores variables that persist during a user's session (while the app is running).

---

## What you need to research (in priority order)

### Must-know (research these)
1. **Streamlit basics** — create an app, display text, buttons, inputs — 20 min
2. **Python requests library** — how to send HTTP requests — 10 min
3. **JSON in Python** — loading/sending JSON data — 5 min

### Good-to-know
4. **Streamlit layout/styling** — columns, sidebars, better-looking layouts — 20 min (optional)
5. **Streamlit session state** — persisting variables across reruns — 10 min (for chat history)

### Don't worry about
- Web design/CSS (Streamlit handles it)
- Backend architecture (Person 4 owns that)

---

## Testing your work (how to know you're done)

Before Phase 1 is complete:

```
1. Can I run the Streamlit app locally?
   → command: streamlit run frontend/app.py
   → Check: does it open in a browser window?

2. Can I type a question and click submit?
   → Check: does the input box work? Does the button respond?

3. Can I call the backend API?
   → You might not have it running yet (Person 4 is building it)
   → For now, hardcode a fake response to test
   → Check: can you display a fake answer + chunks?

4. Does the UI look reasonable?
   → It doesn't need to be pretty, but:
   → Can you read the question easily?
   → Can you read the answer easily?
   → Do the chunks display clearly?
```

**For Phase 1:** Get it working, even if it looks basic. Phase 2 can add styling/polish.

---

## Working without the backend (before Person 4 finishes)

Person 4 might still be building the backend when you want to test. **Hardcode a fake response first:**

```python
# Temporary fake response for testing UI
if st.button("Search"):
    fake_result = {
        "answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without explicit programming.",
        "retrieved_chunks": [
            {
                "chunk_id": "doc1_chunk0",
                "text": "Machine learning involves training algorithms on data...",
                "source_doc": "document1.txt",
                "similarity_score": 0.89
            },
            {
                "chunk_id": "doc2_chunk3",
                "text": "AI and machine learning are transforming industries...",
                "source_doc": "document2.txt",
                "similarity_score": 0.75
            }
        ]
    }
    
    # Display fake result (same code as real result)
    st.subheader("Answer:")
    st.write(fake_result["answer"])
    # ... display chunks ...
```

Once Person 4's backend is ready, replace this with real `query_backend()` calls.

---

## What happens after you're done

Once your frontend works:
- **Person 4** connects it to the real backend
- Users can actually ask questions
- You see real answers (not hardcoded)

Your UI is the face of the entire RAG system. Make it clear and usable.

---

## Common pitfalls to avoid

1. **Hardcoding the backend URL** — use config.py so it's easy to change
2. **Not handling API errors** — what if backend is down? Show an error message, don't crash.
3. **Forgetting to convert similarity scores to float** — JSON might struggle with numpy types
4. **Making the UI too busy** — keep it simple. One input, one answer, one chunk list.

---

## Questions to think about before you start

- [ ] Will I use Streamlit cloud to host it, or run locally? (Phase 1: just local is fine)
- [ ] Do I need chat history? (Phase 1: optional, skip if tight on time)
- [ ] How will I test before Person 4's backend is ready? (Answer: hardcode fake responses)
