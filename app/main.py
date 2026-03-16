import asyncio
import logging

import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.rest import Client as TwilioClient

from app.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POLL_LEAD_ID = 1297347
CALL_TO_NUMBER = "+16475002475"

CALL_QUESTIONS = [
    "What type of legal matter do you need help with?",
    "When did this issue first occur?",
    "Have you spoken with another attorney about this matter?",
    "What is your preferred method of contact?",
    "Are there any upcoming deadlines or court dates?",
    "Is there anything else you'd like us to know?",
]

# Store responses in memory for now
call_responses: dict[str, list[dict]] = {}


def get_twilio_client() -> TwilioClient:
    return TwilioClient(
        settings.twilio_api_key_sid,
        settings.twilio_api_key_secret,
        settings.twilio_account_sid,
    )


def make_twiml_question(question_index: int) -> str:
    """Generate TwiML that asks a question and gathers speech input."""
    question = CALL_QUESTIONS[question_index]
    action_url = f"{settings.public_base_url}/twilio/gather?q={question_index}"
    next_url = f"{settings.public_base_url}/twilio/question?q={question_index + 1}"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" timeout="5" speechTimeout="auto" action="{action_url}">
        <Say voice="Polly.Joanna">{question}</Say>
    </Gather>
    <Say voice="Polly.Joanna">I didn't catch that.</Say>
    <Redirect>{next_url}</Redirect>
</Response>"""


def make_twiml_goodbye() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">Thank you for answering our questions. We will be in touch shortly. Goodbye!</Say>
    <Hangup/>
</Response>"""


def build_inline_twiml() -> str:
    """Build TwiML that asks all questions with pauses for answers."""
    says = "\n".join(
        f'    <Say voice="Polly.Joanna">{q}</Say>\n    <Pause length="5"/>'
        for q in CALL_QUESTIONS
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">Hello, thank you for taking our call. We have a few questions for you.</Say>
    <Pause length="1"/>
{says}
    <Say voice="Polly.Joanna">Thank you for answering our questions. We will be in touch shortly. Goodbye!</Say>
</Response>"""


async def place_call():
    """Place an outbound call via Twilio with inline TwiML."""
    client = get_twilio_client()
    call = client.calls.create(
        to=CALL_TO_NUMBER,
        from_=settings.twilio_phone_number,
        twiml=build_inline_twiml(),
    )
    logger.info("call_placed: sid=%s to=%s", call.sid, CALL_TO_NUMBER)


async def poll_rails_lead():
    """Pull lead data from Rails once on startup."""
    url = f"{settings.rails_base_url}/api/voice/leads/{POLL_LEAD_ID}"
    headers = {"X-Internal-Api-Key": settings.rails_internal_api_key}

    try:
        async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.info("lead_poll_response: %s", data)
    except Exception:
        logger.exception("lead_poll_failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await poll_rails_lead()
    await place_call()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.api_route("/twilio/question", methods=["GET", "POST"])
async def twilio_question(q: int = 0):
    """Serve TwiML for a given question index."""
    if q >= len(CALL_QUESTIONS):
        return Response(content=make_twiml_goodbye(), media_type="application/xml")
    return Response(content=make_twiml_question(q), media_type="application/xml")


@app.post("/twilio/gather")
async def twilio_gather(request: Request, q: int = 0, SpeechResult: str = Form("")):
    """Handle Twilio's gather callback with the caller's speech response."""
    question = CALL_QUESTIONS[q] if q < len(CALL_QUESTIONS) else "unknown"
    logger.info("answer_received: q=%d question='%s' answer='%s'", q, question, SpeechResult)

    # Store the response
    form = await request.form()
    call_sid = form.get("CallSid", "unknown")
    if call_sid not in call_responses:
        call_responses[call_sid] = []
    call_responses[call_sid].append({
        "question": question,
        "answer": SpeechResult,
    })

    # Move to next question
    next_q = q + 1
    if next_q >= len(CALL_QUESTIONS):
        logger.info("call_complete: sid=%s responses=%s", call_sid, call_responses.get(call_sid))
        return Response(content=make_twiml_goodbye(), media_type="application/xml")
    return Response(content=make_twiml_question(next_q), media_type="application/xml")
