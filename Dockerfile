FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY . /app/src

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/src

CMD ["python3", "-m", "bot"]
