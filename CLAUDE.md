# CLAUDE.md

## Project Overview

**voice** is a monorepo with two services:

1. **frontend/** — Next.js app (TypeScript, App Router), deployed to Vercel
2. **api/** — FastAPI app (Python), deployed to GCP Cloud Run, connected to an existing PostgreSQL database

## Architecture

```
voice/
├── frontend/          # Next.js (Vercel)
│   ├── src/app/       # App Router pages and layouts
│   ├── src/components/
│   ├── src/lib/       # Utilities, API client
│   └── package.json
├── api/               # FastAPI (GCP Cloud Run)
│   ├── app/
│   │   ├── main.py    # FastAPI app entry point
│   │   ├── routers/   # API route modules
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── schemas/   # Pydantic request/response schemas
│   │   └── core/      # Config, database connection, dependencies
│   ├── pyproject.toml
│   └── Dockerfile
├── .claude/           # Claude Code settings, skills, commands
├── .serena/           # Serena LSP config (typescript + python)
└── .taskmaster/       # Task Master config
```

## Development Commands

### Frontend
```bash
cd frontend && npm run dev      # Dev server on :3000
cd frontend && npm run build    # Production build
cd frontend && npm run lint     # ESLint
```

### API
```bash
cd api && uv run uvicorn app.main:app --reload   # Dev server on :8000
cd api && uv run pytest                           # Run tests
```

## Claude-Code Behavioral Instructions

### Exploration Phase

Always explore on your own to gain complete understanding. Only delegate to exploration agents if the user explicitly requests it.

## Serena Best Practices

Serena provides semantic code analysis — use it efficiently:

### Intelligent Code Reading Strategy

1. **Start with overview**: Use `get_symbols_overview` to see top-level structure
2. **Target specific symbols**: Use `find_symbol` with `include_body=true` only for symbols you need to understand or edit
3. **Pattern search**: Use `search_for_pattern` for flexible regex-based discovery
4. **Reference tracking**: Use `find_referencing_symbols` to understand usage
5. **Read full files only as a last resort** when symbolic tools cannot provide what you need

### Symbol Navigation

Symbols are identified by `name_path` and `relative_path`:

- Top-level: `ClassName` or `function_name`
- Methods: `ClassName/method_name`
- Nested: `OuterClass/InnerClass/method`
- Python constructors: `ClassName/__init__`

### Efficiency Principles

- Read symbol bodies only when you need to understand or edit them
- Use `depth` parameter to get method lists without bodies: `find_symbol("Foo", depth=1, include_body=False)`
- Track which symbols you've read and reuse that context
- Use symbolic tools before reading full files

## Key Conventions

- **Git commits**: Use conventional commits with scope: `feat(api): add user endpoint`, `fix(frontend): form validation`
- **API communication**: Frontend calls API via `NEXT_PUBLIC_API_URL` env var
- **Database**: Existing PostgreSQL — do NOT create migration scripts that drop/recreate existing tables. Use Alembic for additive migrations only.
- **Environment variables**: Never commit `.env` files. Use `.env.example` as templates.
- **Python deps**: Managed with `uv` (pyproject.toml), not pip
- **Node deps**: Managed with `npm` (package.json)

## Deployment

- **Frontend**: Vercel auto-deploys from `main` branch. Root directory set to `frontend/`.
- **API**: GCP Cloud Run via `gcloud run deploy` or Cloud Build. Dockerfile in `api/`.
- **Database**: Existing PostgreSQL instance — connection via `DATABASE_URL` secret.

## Project Rules

### File Management

- **Edit `tasks.json` only via Task Master commands** — use MCP tools or slash commands
- **Edit `config.json` only via** `/project:tm/models/setup`
- Task markdown files in `.taskmaster/tasks/*.md` are auto-generated

### Permission Configuration

See `.claude/settings.json` for the full tool allowlist/denylist.

### Context Management

- Use `/clear` between different tasks to reset context
- This CLAUDE.md is automatically loaded
- Task Master commands pull task context on demand

### Template Sync

- `.github/template-state.json` tracks template version and configuration variables
- Use Actions → Template Sync to pull upstream configuration updates
- Always review PR changes before merging to preserve local customizations

## Task Master Integration

Task Master is the primary workflow orchestration system. Always prefer MCP tools over CLI commands.

### Working with Tasks

1. Parse requirements: `/project:tm/parse-prd .taskmaster/docs/prd.txt`
2. Analyze complexity: `/project:tm/analyze-complexity --research`
3. Expand tasks: `/project:tm/expand/all`
4. Get next task: `/project:tm/next`
5. Update progress: Use MCP `update_subtask` to log implementation notes
6. Complete: `/project:tm/set-status/to-done <id>`

See `.taskmaster/CLAUDE.md` for the complete Task Master integration guide.

**IMPORTANT!!! Import Task Master's development workflow commands and guidelines, treat as if import is in the main CLAUDE.md file.**

@./.taskmaster/CLAUDE.md
