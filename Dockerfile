FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /workspace

COPY pyproject.toml .
COPY uv.lock .

COPY app/ app/
COPY data/ data/
COPY README.md .

RUN uv sync --frozen --no-dev


ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "python", "app/bot.py"]
