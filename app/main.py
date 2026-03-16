import asyncio
import logging

import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POLL_LEAD_ID = 1297347
POLL_INTERVAL_SECONDS = 1


async def poll_rails_lead():
    url = f"{settings.rails_base_url}/api/voice/leads/{POLL_LEAD_ID}"
    headers = {"X-Internal-Api-Key": settings.rails_internal_api_key}

    while True:
        try:
            async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.info("lead_poll_response: %s", data)
        except Exception:
            logger.exception("lead_poll_failed")

        await asyncio.sleep(POLL_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(poll_rails_lead())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}
