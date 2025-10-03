from openai import OpenAI
from typing import List, Dict
from .config import settings

_client = OpenAI(
    base_url=settings.nebius_base_url,
    api_key=settings.nebius_api_key,
)

def chat(
    messages: List[Dict[str, str]],
    max_tokens: int,
    temperature: float | None = None,
    model: str | None = None,
) -> str:
    resp = _client.chat.completions.create(
        model=model or settings.llm_model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature if temperature is not None else settings.llm_temperature,
    )
    return resp.choices[0].message.content
