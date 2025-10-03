import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    allowed_chat_ids: list[int] = (
        [int(x) for x in os.getenv("ALLOWED_CHAT_IDS", "").split(",") if x.strip()]
        if os.getenv("ALLOWED_CHAT_IDS") else []
    )

    # Nebius / OpenAI API
    nebius_api_key: str = os.getenv("NEBIUS_API_KEY", "")
    nebius_base_url: str = os.getenv("NEBIUS_BASE_URL", "https://api.studio.nebius.com/v1/")

    llm_model: str = os.getenv("LLM_MODEL", "Qwen/Qwen3-14B")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    summarize_max_tokens: int = int(os.getenv("SUMMARIZE_MAX_TOKENS", "128"))
    select_max_tokens: int = int(os.getenv("SELECT_MAX_TOKENS", "12"))

    embed_model_name: str = os.getenv("EMBED_MODEL_NAME", "BAAI/bge-m3")
    top_k: int = int(os.getenv("TOP_K", "8"))
    n_candidates_for_llm: int = int(os.getenv("N_CANDIDATES_FOR_LLM", "5"))

settings = Settings()
