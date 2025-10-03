from openai import OpenAI
import numpy as np
from typing import List

from app.core import settings

_client = OpenAI(
    base_url=settings.nebius_base_url,
    api_key=settings.nebius_api_key,
)

def embed_texts(texts: List[str], model: str | None = None) -> np.ndarray:
    """
    Получить эмбеддинги через Nebius Embeddings API.
    """
    resp = _client.embeddings.create(
        model=model or settings.embed_model_name,
        input=texts
    )
    vectors = [d.embedding for d in resp.data]
    return np.array(vectors, dtype=np.float32)

def embed_text(text: str, model: str | None = None) -> np.ndarray:
    return embed_texts([text], model=model)[0]
