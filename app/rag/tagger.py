from app.core import chat

TAG_PROMPT = """
Сгенерируй 3–6 тегов (одно-два слова) для этого текста.
Только слова через запятую, без пояснений.
Текст: "{post}"
"""

def generate_tags_for_post(text: str) -> list[str]:
    resp = chat(
        [
            {"role": "system", "content": "Ты выделяешь ключевые смыслы и эмоции из текста."},
            {"role": "user", "content": TAG_PROMPT.format(post=text)}
        ],
        max_tokens=50,
    )
    return [t.strip() for t in resp.split(",") if t.strip()]
