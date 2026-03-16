# Voice

FastAPI service for the voice lead-pulling pipeline.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Run

```bash
uv run uvicorn app.main:app --reload
```

The server starts on `http://127.0.0.1:8000`. You should see a counter logging every second in the terminal.

## Health Check

```bash
curl http://127.0.0.1:8000/health
```
