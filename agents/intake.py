import json
import logging
from datetime import datetime

from .base import Agent

logger = logging.getLogger(__name__)

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
                "full_name": {"type": "string", "description": "Caller's full name"},
                "date_of_birth": {"type": "string", "description": "Caller's date of birth"},
                "reason_for_visit": {"type": "string", "description": "Why the caller wants to be seen"},
                "callback_number": {"type": "string", "description": "Phone number to call back"},
                "preferred_time": {"type": "string", "description": "Preferred day and time for follow-up"},
            },
            "required": ["full_name", "date_of_birth", "reason_for_visit", "callback_number", "preferred_time"],
        },
    },
}


class IntakeAgent(Agent):
    name = "intake"
    system_prompt = SYSTEM_PROMPT
    tools = [INTAKE_TOOL]

    def handle_tool_call(self, name: str, args: dict) -> tuple[str, dict | None]:
        if name == "save_intake":
            intake = {
                **args,
                "created_at": datetime.now().isoformat(),
            }
            logger.info(f"Intake saved: {json.dumps(intake, indent=2)}")
            return (
                "Intake information saved successfully. The patient will receive a callback to confirm their appointment.",
                args,
            )
        return ("Unknown tool", None)
