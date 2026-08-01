from pathlib import Path

def load_documents(data_folder_path):
    """Read all .txt files from the data folder."""
    folder = Path(data_folder_path)
    documents = []
    for file_path in folder.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")
        documents.append((file_path.name, content))
    return documents