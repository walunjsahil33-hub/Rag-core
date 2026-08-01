import json
from pathlib import Path
from data_loader import load_documents
from chunking import chunk_text
from embeddings import generate_embeddings

def main():
    data_path = Path("data")
    if not data_path.exists():
        print("Error: 'data/' folder not found.")
        return

    documents = load_documents(data_path)
    all_chunk_data = []

    for filename, content in documents:
        chunks = chunk_text(content, chunk_size=500, overlap=50)
        embeddings = generate_embeddings(chunks)
        
        for idx, (chunk_str, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_object = {
                "chunk_id": f"{Path(filename).stem}_chunk{idx}",
                "text": chunk_str,
                "source_doc": filename,
                "chunk_position": idx,
                "embedding": embedding
            }
            all_chunk_data.append(chunk_object)

    # Save to project root matching the data contract
    output_file = Path("embeddings.json")
    output_file.write_text(json.dumps(all_chunk_data, indent=2), encoding="utf-8")
    print(f"Success! Created {len(all_chunk_data)} total chunks saved to {output_file.name}")

if __name__ == "__main__":
    main()
    