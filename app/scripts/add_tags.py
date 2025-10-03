import json
import os
from app.core import chat

TAG_PROMPT = """
Сгенерируй 3–6 ключевых тегов по смыслу этой цитаты.
Только слова через запятую, без лишнего текста.
Цитата: "{quote}"
"""

def generate_tags(quote: str) -> list[str]:
    resp = chat(
        [
            {"role": "system", "content": "Ты создаёшь теги для поиска по цитатам."},
            {"role": "user", "content": TAG_PROMPT.format(quote=quote)}
        ],
        max_tokens=50,
    )
    return [t.strip() for t in resp.split(",") if t.strip()]

def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "quotes.json")

    with open(data_path, "r", encoding="utf-8") as f:
        quotes = json.load(f)

    for q in quotes:
        if "tags" not in q or not q["tags"]:
            q["tags"] = generate_tags(q["quote"])
            print(f"{q['id']}: {q['tags']}")

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

    print("✅ Теги добавлены в quotes.json")

if __name__ == "__main__":
    main()
