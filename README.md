# voice

Monorepo with a Next.js frontend (Vercel) and Python FastAPI backend (GCP), connected to an existing PostgreSQL database.

## Structure

```
voice/
├── frontend/     # Next.js (TypeScript) — deployed to Vercel
├── api/          # FastAPI (Python) — deployed to GCP Cloud Run
├── .claude/      # Claude Code configuration
├── .serena/      # Serena LSP configuration
└── .taskmaster/  # Task Master configuration
```

## Getting Started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### API

```bash
cd api
uv sync
uv run uvicorn app.main:app --reload
```

## Environment Variables

Copy `.env.example` to `.env` in each service directory and fill in the values.
