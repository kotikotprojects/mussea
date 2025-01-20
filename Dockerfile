FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY . /app

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python3", "-m", "bot"]
