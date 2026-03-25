import json
import logging
import uuid
from datetime import datetime

from fastapi import FastAPI, Request
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
openai_client = OpenAI()

# In-memory conversation store keyed by session_id
conversations: dict[str, list[dict]] = {}


@app.on_event("startup")
async def startup():
    logger.info("Hello, World! Voice intake server is running.")


SYSTEM_PROMPT = """You are a friendly intake assistant for a medical clinic. Your job is to collect basic information from the caller for a follow-up appointment.

You must collect the following information:
1. Full name
2. Date of birth
3. Reason for visit
4. Preferred callback number (confirm the number they're calling from or get a new one)
5. Preferred day/time for a follow-up appointment

Be conversational and warm. After collecting all the information, use the "save_intake" tool to save it. Then thank them and let them know someone will call back to confirm their appointment."""

INTAKE_TOOL = {
    "type": "function",
    "function": {
        "name": "save_intake",
        "description": "Save the caller's intake information after collecting all required fields.",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {
                    "type": "string",
                    "description": "Caller's full name",
                },
                "date_of_birth": {
                    "type": "string",
                    "description": "Caller's date of birth",
                },
                "reason_for_visit": {
                    "type": "string",
                    "description": "Why the caller wants to be seen",
                },
                "callback_number": {
                    "type": "string",
                    "description": "Phone number to call back",
                },
                "preferred_time": {
                    "type": "string",
                    "description": "Preferred day and time for follow-up",
                },
            },
            "required": [
                "full_name",
                "date_of_birth",
                "reason_for_visit",
                "callback_number",
                "preferred_time",
            ],
        },
    },
}


@app.get("/")
async def health():
    return {"status": "ok"}


@app.post("/test/chat")
async def test_chat(request: Request):
    """Text-based test endpoint for the intake conversation.

    Send JSON: {"message": "your text", "session_id": "optional-existing-id"}
    Returns: {"session_id": "...", "reply": "assistant response", "intake": null | {...}}
    """
    body = await request.json()
    user_message = body.get("message", "")
    session_id = body.get("session_id") or str(uuid.uuid4())

    # Initialize conversation with system prompt if new session
    if session_id not in conversations:
        conversations[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

    messages = conversations[session_id]
    messages.append({"role": "user", "content": user_message})

    intake_data = None

    # Loop to handle tool calls — the model may call a tool before replying
    while True:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=[INTAKE_TOOL],
        )

        choice = response.choices[0]
        assistant_message = choice.message

        # Append the raw assistant message to history
        messages.append(assistant_message.model_dump(exclude_none=True))

        if choice.finish_reason == "tool_calls" and assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                if tool_call.function.name == "save_intake":
                    args = json.loads(tool_call.function.arguments)
                    # Reuse existing save logic (pass a fake message with no call info)
                    result = save_intake(args, {"call": {"customer": {"number": "test"}}})
                    intake_data = args
                else:
                    result = "Unknown tool"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
            # Continue the loop so the model generates a user-facing reply after the tool call
            continue

        # No more tool calls — we have the final text reply
        break

    reply = assistant_message.content or ""
    conversations[session_id] = messages

    return {"session_id": session_id, "reply": reply, "intake": intake_data}


@app.delete("/test/chat/{session_id}")
async def delete_test_session(session_id: str):
    """Delete a test conversation session."""
    conversations.pop(session_id, None)
    return {"status": "deleted"}


@app.post("/webhook")
async def vapi_webhook(request: Request):
    body = await request.json()
    message = body.get("message", {})
    message_type = message.get("type")

    logger.info(f"Received webhook: {message_type}")

    match message_type:
        case "assistant-request":
            return handle_assistant_request(message)
        case "tool-calls":
            return handle_tool_calls(message)
        case "status-update":
            handle_status_update(message)
        case "end-of-call-report":
            handle_end_of_call_report(message)

    return {}


def handle_assistant_request(message: dict) -> dict:
    customer = message.get("call", {}).get("customer", {})
    caller_number = customer.get("number", "unknown")
    logger.info(f"Inbound call from {caller_number}")

    return {
        "assistant": {
            "firstMessage": "Hi there! Thanks for calling. I'd love to help get you set up for a follow-up appointment. Can I start with your full name?",
            "model": {
                "provider": "openai",
                "model": "gpt-4o",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}],
                "tools": [INTAKE_TOOL],
            },
            "voice": {
                "provider": "11labs",
                "voiceId": "21m00Tcm4TlvDq8ikWAM",
            },
        }
    }


def handle_tool_calls(message: dict) -> dict:
    results = []
    tool_call_list = message.get("toolCallList", [])

    for tool_call in tool_call_list:
        tool_call_id = tool_call.get("id")
        name = tool_call.get("name")
        args = tool_call.get("arguments", {})

        if name == "save_intake":
            result = save_intake(args, message)
            results.append({"toolCallId": tool_call_id, "result": result})
        else:
            results.append({"toolCallId": tool_call_id, "result": "Unknown tool"})

    return {"results": results}


def save_intake(args: dict, message: dict) -> str:
    customer = message.get("call", {}).get("customer", {})
    caller_number = customer.get("number", "unknown")

    intake = {
        "full_name": args.get("full_name"),
        "date_of_birth": args.get("date_of_birth"),
        "reason_for_visit": args.get("reason_for_visit"),
        "callback_number": args.get("callback_number", caller_number),
        "preferred_time": args.get("preferred_time"),
        "caller_number": caller_number,
        "created_at": datetime.now().isoformat(),
    }

    logger.info(f"Intake saved: {json.dumps(intake, indent=2)}")

    # TODO: persist to a database
    return "Intake information saved successfully. The patient will receive a callback to confirm their appointment."


def handle_status_update(message: dict):
    status = message.get("status")
    call_id = message.get("call", {}).get("id", "unknown")
    logger.info(f"Call {call_id} status: {status}")


def handle_end_of_call_report(message: dict):
    call = message.get("call", {})
    call_id = call.get("id", "unknown")
    ended_reason = message.get("endedReason", "unknown")
    artifact = message.get("artifact", {})
    transcript = artifact.get("transcript", "")

    logger.info(f"Call {call_id} ended: {ended_reason}")
    logger.info(f"Transcript:\n{transcript}")
