from rapidfuzz import fuzz
from typing import List, Dict, Any

def rerank_by_keyword_hint(summary: str, candidates: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    pairs = []
    for c in candidates:
        score = fuzz.token_set_ratio(summary, c["quote"])
        pairs.append((score, c))
    pairs.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in pairs[:top_n]]
