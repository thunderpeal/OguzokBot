import faiss
import os
import json
from pathlib import Path


from app.core import embed_texts, embed_text

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
QUOTES_PATH = os.path.join(DATA_DIR, "quotes.json")
INDEX_PATH = os.path.join(DATA_DIR, "quotes.index")
META_PATH = os.path.join(DATA_DIR, "quotes.meta.json")

def build_index():
    with open(QUOTES_PATH, "r", encoding="utf-8") as f:
        quotes = json.load(f)

    texts = [
        q["quote"] + " " + " ".join(q.get("tags", []))
        for q in quotes
    ]
    embeddings = embed_texts(texts)
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

def ensure_index():
    if not (os.path.exists(INDEX_PATH) and os.path.exists(META_PATH)):
        build_index()

class QuoteStore:
    def __init__(self):
        self.index = None
        self.meta = []

    def load(self):
        self.index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "r", encoding="utf-8") as f:
            self.meta = json.load(f)

    def search(self, query: str, top_k: int = 5):
        q_vec = embed_text(query).reshape(1, -1)
        faiss.normalize_L2(q_vec)
        scores, idxs = self.index.search(q_vec, top_k)
        results = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx < 0:
                continue
            item = {
                "id": self.meta[idx]["id"],
                "quote": self.meta[idx]["quote"]
            }
            results.append((float(score), item))
        return results

