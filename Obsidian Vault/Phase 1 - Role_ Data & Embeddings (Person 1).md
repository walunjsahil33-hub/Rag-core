---
tags: [rag-core, phase-1, person-1, data, embeddings]
parent: [[Phase 1 Overview]]
---

# Phase 1 — Role: Data & Embeddings (Person 1)

## Your Mission

You are responsible for transforming raw documents into a format the rest of the system can search. Specifically:
1. Load documents from files
2. Split them into searchable chunks
3. Convert chunks into embeddings (numbers that capture meaning)
4. Save everything to a JSON file that Person 2, 3, and 4 will use

**You are the gatekeeper of data.** If your chunks are bad, retrieval is bad, answers are bad. So understanding *why* you chunk the way you do matters.

---

## What you'll build (Concrete deliverable)

**Input:** A folder of `.txt` files with sample documents
**Output:** A single `embeddings.json` file with this structure:

```json
[
  {
    "chunk_id": "doc1_chunk0",
    "text": "This is the first chunk of text from document 1...",
    "source_doc": "document1.txt",
    "chunk_position": 0,
    "embedding": [0.123, -0.456, 0.789, ...]  // 384 numbers for this embedding model
  },
  {
    "chunk_id": "doc1_chunk1",
    "text": "This is the second chunk...",
    "source_doc": "document1.txt",
    "chunk_position": 1,
    "embedding": [0.234, -0.567, 0.890, ...]
  }
]
```

This JSON file is the **source of truth** for the rest of the pipeline. Person 2 will load this, Person 4 will pass it to the LLM, Person 3 will display it.

---

## Code structure you'll create

```
project-root/
├── data/
│   ├── sample_doc1.txt
│   ├── sample_doc2.txt
│   └── sample_doc3.txt
└── retrieval/
    ├── __init__.py
    ├── data_loader.py         # Load .txt files
    ├── chunking.py            # Split into chunks
    ├── embeddings.py          # Generate embeddings
    └── generate_embeddings.py # Main script that ties it together
```

**Each file has a single responsibility:**
- `data_loader.py` — reads files, returns text
- `chunking.py` — takes text, splits into chunks, returns list of chunks
- `embeddings.py` — takes chunks, converts to embeddings, returns enriched chunks
- `generate_embeddings.py` — orchestrates: load → chunk → embed → save to JSON

---

## Step-by-step what you'll code

### Step 1: Load documents

**File:** `retrieval/data_loader.py`

```python
def load_documents(data_folder_path):
    """
    Read all .txt files from a folder.
    
    Input: path to folder containing .txt files
    Output: list of tuples: [(filename, content), (filename, content), ...]
    """
    # pseudocode:
    # loop through all files in folder
    # if file ends with .txt, read it
    # return list of (filename, content)
```

**What you need to understand:** How to read files in Python (the `open()` function, or use `pathlib` library)

**Depth needed:** Basic — just know how to read a text file and get its content as a string.

**Research:** Search "Python read text file" — that's literally all you need to know.

---

### Step 2: Chunk text

**File:** `retrieval/chunking.py`

```python
def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split a long text into smaller overlapping chunks.
    
    Input: 
      - text: the full document as a string
      - chunk_size: how many characters per chunk (500 means ~100 words)
      - overlap: how many characters to repeat between chunks (50 means chunks overlap by 50 chars)
    
    Output: list of chunks, each a string
    
    Example:
      text = "The quick brown fox jumps over the lazy dog. The dog sleeps."
      chunks = chunk_text(text, chunk_size=30, overlap=5)
      # Returns: ["The quick brown fox jumps ...", "jumps over the lazy dog. The...", ...]
    """
    # pseudocode:
    # start at position 0
    # take 500 characters, make a chunk
    # move forward 450 characters (overlap=50, so 500-50=450)
    # repeat until you run out of text
```

**What you need to understand:** 
- Why chunk? Documents are too long for LLMs to process at once. Chunking makes them bite-sized.
- Why overlap? If you cut at random positions, you might split a sentence in half. Overlapping ensures concepts aren't lost at chunk boundaries.
- Fixed-size vs. semantic chunking: We're doing fixed-size for Phase 1 (simpler). Sentence-based chunking comes in Phase 2.

**Depth needed:** Shallow — understand the "why" above, don't overthink the math.

**Research:** Search "text chunking for RAG" — you'll see that 300-1000 characters per chunk is standard. Just pick a size (try 500) and see if it works.

---

### Step 3: Generate embeddings

**File:** `retrieval/embeddings.py`

```python
from sentence_transformers import SentenceTransformer

def generate_embeddings(chunks):
    """
    Convert text chunks into embeddings (number vectors).
    
    Input: list of chunk texts
    Output: list of embeddings, where each embedding is a list of 384 numbers
    
    Example:
      chunks = ["hello world", "goodbye world"]
      embeddings = generate_embeddings(chunks)
      # Returns: [[0.1, 0.2, ..., 0.384], [-0.1, 0.3, ..., -0.2]]
    """
    # pseudocode:
    # load the pre-trained model (all-MiniLM-L6-v2)
    # for each chunk in chunks:
    #   pass it to the model
    #   model returns a list of 384 numbers
    #   save those numbers
    # return list of all embeddings
```

**What you need to understand:**
- What is an embedding? It's a way to represent text as numbers. Similar text → similar numbers.
- Why sentence-transformers? It's already trained on millions of texts, so it understands meaning.
- The model (all-MiniLM-L6-v2) returns exactly 384 numbers per chunk. Don't change that.

**Depth needed:** Just enough to use the library. You don't need to understand *how* the model works inside (that's transformer neural networks, deep stuff). Just: put text in → get 384 numbers out.

**Research:** Search "sentence-transformers tutorial" or look at their GitHub README. Copy-paste their "Getting Started" example. It's literally 5 lines of code:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')  # downloads model on first run (~50MB)
embeddings = model.encode(["hello world", "goodbye world"])  # returns 2x384 numbers
```

---

### Step 4: Orchestrate & save to JSON

**File:** `retrieval/generate_embeddings.py`

```python
import json
from data_loader import load_documents
from chunking import chunk_text
from embeddings import generate_embeddings

def main():
    """
    Orchestrate: load docs → chunk → embed → save to JSON
    """
    # pseudocode:
    # 1. load documents from /data folder
    # 2. for each document:
    #    - chunk it
    #    - generate embeddings for each chunk
    #    - create a chunk object: {chunk_id, text, source_doc, embedding}
    # 3. save all chunks as JSON
    # 4. print how many chunks were created

if __name__ == "__main__":
    main()
```

**Output:** A file called `embeddings.json` in the root of the project with all chunks + embeddings.

---

## What you need to research (in priority order)

### Must-know (research these, understand 80%)
1. **How to read files in Python** — 10 min read/watch
2. **String manipulation in Python** — slicing, substring operations — 15 min
3. **sentence-transformers basic usage** — load model, encode text — 20 min
4. **JSON format and how to save/load JSON in Python** — 10 min

### Good-to-know (research if curious, but not required)
5. **What embeddings actually are** — search "embeddings explained simply" (30 min optional video)
6. **Chunking strategies** — why overlap matters, why size matters (20 min optional read)

### Don't worry about (not needed for Phase 1)
- How transformers work inside
- Why all-MiniLM-L6-v2 is good (trust that it is)
- Optimizing embeddings

---

## Testing your work (how to know you're done)

Before you hand off to Person 2, run this mentally:

```python
# 1. Can I load a document from /data folder? 
#    → Try opening a sample .txt file, print its content

# 2. Can I chunk it?
#    → Run chunk_text() on a document, print the chunks, 
#      check: is each chunk ~500 chars? Do they overlap?

# 3. Can I generate embeddings?
#    → Run generate_embeddings() on 1-2 chunks, print the embedding
#      check: is it a list of 384 numbers?

# 4. Can I save to JSON?
#    → Run generate_embeddings.py fully, check: does embeddings.json exist?
#      check: can I load it back with json.load()? Does it have the right structure?

# 5. Check the numbers
#    → How many chunks did you create? (aim for 20-50 chunks across 3-5 documents)
#    → How many embeddings? (should equal number of chunks)
```

**You're done when:** embeddings.json exists, has the right structure, and Person 2 can load it and use it.

---

## Questions to think about before you start

- [ ] Which 3-5 documents will we use? (What folder path will they be in?)
- [ ] What chunk size should we try first? (500 is a good starting point)
- [ ] Should we use overlap? (Yes, try 50 characters overlap)
- [ ] How will I test my code? (Create a few test .txt files first)

---

## What happens after you're done

Once your `embeddings.json` is ready:
- **Person 2** loads it and builds a function that finds similar chunks
- **Person 4** will take those chunks and pass them to the LLM
- Everyone benefits from good, clean data

So spend time on this — bad chunks now = bad answers later. It's worth 2-3 hours of focus to get it right.
