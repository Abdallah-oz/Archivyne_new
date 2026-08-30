FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-install-project

COPY . .

CMD ["uv", "run", "fastapi", "run", "src/backend/main.py", "--host", "0.0.0.0", "--port", "8000"]