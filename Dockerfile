FROM ghcr.io/astral-sh/uv:python3.15-alpine
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
RUN uv sync --no-dev
CMD ["uv", "run", "recurse-cv-server"]
