FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY sql ./sql
COPY data ./data

RUN pip install --upgrade pip && pip install -e ".[dev]"

CMD ["python", "-m", "fund_finance.cli", "--help"]
