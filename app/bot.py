import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.core import settings, SELECT_PROMPT, chat, rerank_by_keyword_hint
from app.rag import QuoteStore, ensure_index, generate_tags_for_post

# === Логирование ===
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger("quote-bot")

router = Router()
dp = Dispatcher()
dp.include_router(router)

bot = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)

quote_store = QuoteStore()


@router.message(F.reply_to_message.is_(None))
async def handle_channel_post(message: types.Message):
    chat_id = message.chat.id
    logger.info(f"Получен новый пост из канала {chat_id}")

    text = message.text or message.caption

    if not text:
        logger.info("Пропущено: пост без текста/подписи")
        return

    tags = generate_tags_for_post(text)
    query_text = text + " " + " ".join(tags)

    try:
        results = quote_store.search(query_text, top_k=settings.top_k)
        logger.debug(results)
        candidates = [q for _, q in results]

        candidates = rerank_by_keyword_hint(query_text, candidates, top_n=settings.n_candidates_for_llm)
        logger.info(f"Найдено {len(candidates)} кандидатов для выбора")
        logger.debug(candidates)

        if not candidates:
            logger.warning("Нет кандидатов для цитаты")
            return

        # 3) Финальный выбор
        numbered = [(i + 1, c) for i, c in enumerate(candidates)]
        candidates_str = "\n".join([f'{i}. "{c["quote"]}"' for i, c in numbered])

        selection_raw = chat(
            [
                {"role": "system", "content": "Отвечай строго JSON, без лишнего текста и разметки! Только сам JSON."},
                {"role": "user", "content": SELECT_PROMPT.format(post=text, candidates=candidates_str)},
            ],
            max_tokens=settings.select_max_tokens,
        )
        logger.debug(f"Ответ модели выбора: {selection_raw}")

        try:
            idx = int(json.loads(selection_raw).get("index"))
        except Exception as e:
            logger.warning(f"Ошибка парсинга JSON от модели: {e}. Выбираем первого кандидата.")
            idx = 1

        if idx < 1 or idx > len(candidates):
            return

        best = numbered[idx - 1][1]
        logger.info(f"Выбрана цитата: {best['id']} → {best['quote']}")

        await message.reply(best["quote"])

    except Exception as e:
        logger.exception(f"Ошибка при обработке поста: {e}")


async def main():
    logger.info("Запуск бота...")
    ensure_index()
    quote_store.load()
    logger.info("Индекс цитат загружен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
