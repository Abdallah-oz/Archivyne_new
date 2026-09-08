FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-install-project

COPY . .

CMD ["sh", "-c", "cd /app/src/backend && uv run alembic upgrade head && cd /app && exec uv run fastapi run src/backend/main.py --host 0.0.0.0 --port ${PORT:-8000}"]