# Voice

FastAPI service for the voice lead-pulling pipeline. Pulls lead data from Rails, then places a Twilio call to ask intake questions via speech.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- [Node.js](https://nodejs.org/) (for localtunnel)
- A `.env` file (see below)

## Setup

```bash
uv sync
```

Copy `.env.example` to `.env` and fill in your values:

```
RAILS_BASE_URL=https://app.lvh.me:3443
RAILS_INTERNAL_API_KEY=<shared key with Rails>

TWILIO_ACCOUNT_SID=<your AC... SID>
TWILIO_API_KEY_SID=<your SK... key>
TWILIO_API_KEY_SECRET=<your API key secret>
TWILIO_PHONE_NUMBER=<your Twilio number>
OPENAI_API_KEY=<your OpenAI key>

PUBLIC_BASE_URL=<localtunnel URL, set after starting tunnel>
```

## Run

Three terminals are needed:

### Terminal 1 — Start the tunnel

Twilio needs a public URL to reach your local server for webhooks.

```bash
npx localtunnel --port 8000
```

Copy the URL it prints (e.g. `https://xxxx.loca.lt`) and set `PUBLIC_BASE_URL` in your `.env`.

### Terminal 2 — Start Rails (in the storefront repo)

```bash
direnv allow
bin/dev
```

### Terminal 3 — Start FastAPI

```bash
uv run uvicorn app.main:app --reload
```

On startup the server will:
1. Pull lead data from Rails
2. Place a Twilio call to the configured number
3. Ask 6 intake questions, gathering speech responses
4. Log all answers to the console

## Health Check

```bash
curl http://127.0.0.1:8000/health
```
