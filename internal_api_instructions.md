# Internal API V1 Implementation Guide
> Instructions for Claude Code to implement the Rails internal endpoint and FastAPI lead-pulling service.

---

## Overview

Build a clean internal API bridge between Rails and FastAPI using shared API key authentication. Do **not** modify or repurpose the existing Chrome controller.

---

## Step 1 — Add Rails Route

In `config/routes.rb`, inside the existing `namespace :api` block, add:

```ruby
namespace :api do
  # ... existing routes ...
  namespace :voice do
    resources :leads, only: [:show]
  end
end
```

This exposes: `GET /api/voice/leads/:id`

---

## Step 2 — Create the Rails Controller

Create file: `app/controllers/api/voice/leads_controller.rb`

```ruby
# frozen_string_literal: true

# Api::Voice::LeadsController
# Internal API endpoint for the FastAPI voice service to pull lead data.
# Authentication is via shared API key (X-Internal-Api-Key header) — no session/cookie auth.
# Endpoints:
#   GET /api/voice/leads/:id - Single lead with full details

module Api
  module Voice
    class LeadsController < ApplicationController
      skip_before_action :verify_authenticity_token
      skip_before_action :track_ahoy_visit, if: -> { self.class.method_defined?(:track_ahoy_visit) }
      before_action :verify_internal_api_key!

      # GET /api/voice/leads/:id
      def show
        lead = Lead.includes(:campaign, :journey, :responses).find_by(id: params[:id])
        return render json: { error: "Lead not found" }, status: :not_found unless lead.present?

        render json: {
          id: lead.id,
          law_firm_id: lead.law_firm_id,
          first_name: lead.first_name,
          middle_name: lead.middle_name,
          last_name: lead.last_name,
          full_name: lead.full_name,
          email: lead.email,
          phone: lead.phone,
          company: lead.company,
          consent_status: lead.consent_status,

          status: lead.status,
          completed: lead.completed?,
          read: lead.read?,
          completed_at: lead.completed_at,
          completion_time: lead.completion_time,

          funnel: lead.campaign&.name,
          workflow: lead.journey&.name,

          source: lead.source,
          referrer: lead.referrer,

          engaged_clip: lead.engaged_clip&.name,
          landing_page: lead.landing_page&.full_url,
          landed_url: lead.landed_url,

          responses: lead.responses&.map { |r|
            {
              question_body: r.question_body,
              answer: r.display_value
            }
          },

          integration_status: lead.integration_status
        }
      end

      private

      def verify_internal_api_key!
        provided = request.headers["X-Internal-Api-Key"].to_s
        expected = ENV["FASTAPI_INTERNAL_API_KEY"].to_s

        unless provided.present? && expected.present? &&
               ActiveSupport::SecurityUtils.secure_compare(provided, expected)
          render json: { error: "Unauthorized" }, status: :unauthorized
        end
      end
    end
  end
end
```

---

## Step 3 — Add Rails Environment Variable

In your Rails `.env` (or credentials/secrets), add:

```
FASTAPI_INTERNAL_API_KEY=super-secret-shared-key
```

> Use a strong random value in production. This key must match on both sides.

---

## Step 4 — Scaffold the FastAPI Project

```bash
uv init fastapi-lead-puller
cd fastapi-lead-puller
uv add fastapi uvicorn httpx pydantic-settings
```

Create the following directory structure:

```
app/
  __init__.py
  main.py
  settings.py
  routers/
    __init__.py
    leads.py
  services/
    __init__.py
    rails_client.py
.env
```

---

## Step 5 — FastAPI Settings

Create `app/settings.py`:

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rails_base_url: str
    rails_internal_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
```

Create `.env`:

```
RAILS_BASE_URL=http://localhost:3000
RAILS_INTERNAL_API_KEY=super-secret-shared-key
```

---

## Step 6 — FastAPI Rails Client

Create `app/services/rails_client.py`:

```python
import httpx
from app.settings import settings


async def fetch_lead_from_rails(lead_id: int) -> dict:
    url = f"{settings.rails_base_url}/api/voice/leads/{lead_id}"
    headers = {
        "X-Internal-Api-Key": settings.rails_internal_api_key
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
```

---

## Step 7 — FastAPI Router

Create `app/routers/leads.py`:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from app.services.rails_client import fetch_lead_from_rails

router = APIRouter()
logger = logging.getLogger(__name__)


class PullLeadRequest(BaseModel):
    lead_id: int


@router.post("/test/pull-lead")
async def pull_lead(request: PullLeadRequest):
    try:
        lead_data = await fetch_lead_from_rails(request.lead_id)
    except Exception as e:
        logger.exception("lead_pull_failed")
        raise HTTPException(status_code=502, detail=f"Failed to fetch lead: {str(e)}")

    logger.info(
        "lead_pull_success",
        extra={
            "lead_id": lead_data.get("id"),
            "law_firm_id": lead_data.get("law_firm_id"),
            "has_phone": bool(lead_data.get("phone")),
            "has_email": bool(lead_data.get("email")),
            "response_count": len(lead_data.get("responses", [])),
            "status": lead_data.get("status"),
        },
    )

    return {
        "ok": True,
        "lead_id": lead_data.get("id"),
        "law_firm_id": lead_data.get("law_firm_id"),
    }
```

---

## Step 8 — FastAPI App Entrypoint

Create `app/main.py`:

```python
from fastapi import FastAPI
from app.routers.leads import router as leads_router

app = FastAPI()
app.include_router(leads_router)
```

---

## Step 9 — Run FastAPI

```bash
uv run uvicorn app.main:app --reload
```

---

## Step 10 — Test the Full Flow

With Rails running on port 3000 and FastAPI on port 8000:

```bash
curl -X POST http://127.0.0.1:8000/test/pull-lead \
  -H "Content-Type: application/json" \
  -d '{"lead_id": 123}'
```

Expected response:

```json
{
  "ok": true,
  "lead_id": 123,
  "law_firm_id": 88
}
```

---

## Key Constraints

- **Do not** modify or call the Chrome controller (`/api/chrome/leads`) from FastAPI.
- **Do not** use session cookie auth or `current_user` in the internal endpoint.
- The internal endpoint must be protected solely via `X-Internal-Api-Key` header.
- Log only safe fields in production — never log full payload with PII.

---

## Expected Rails JSON Response Shape

```json
{
  "id": 123,
  "law_firm_id": 88,
  "first_name": "Jane",
  "middle_name": null,
  "last_name": "Doe",
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+14165551234",
  "company": "Acme Inc",
  "consent_status": "unknown",
  "status": "new",
  "completed": true,
  "read": false,
  "completed_at": "2026-03-16T15:00:00Z",
  "completion_time": 45,
  "funnel": "Estate Planning Funnel",
  "workflow": "Manual Intake Workflow",
  "source": "Manual Input",
  "referrer": "Direct",
  "engaged_clip": null,
  "landing_page": "https://example.com/intake",
  "landed_url": "https://example.com/intake?src=test",
  "responses": [
    {
      "question_body": "What type of matter do you need help with?",
      "answer": "Estate planning"
    }
  ],
  "integration_status": "pending"
}
```

---

## Future Work (Post V1)

Once the above is verified working, add a `lead_pull_events` audit table with:

| Column | Type |
|---|---|
| id | integer |
| lead_id | integer |
| law_firm_id | integer |
| status | string |
| payload_json | jsonb |
| error_message | text |
| created_at | timestamp |

This provides a verifiable audit trail before adding Twilio or OpenAI integrations.
