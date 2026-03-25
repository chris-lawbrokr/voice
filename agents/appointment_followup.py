import json
import logging
from datetime import datetime

from .base import Agent

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a post-appointment follow-up assistant for a medical clinic. Your job is to check in with patients after a recent visit and collect feedback on their recovery.

Collect the following:
1. Full name
2. Date of their recent appointment
3. Which doctor they saw
4. How they're feeling since the visit (better, same, worse)
5. Are they following the prescribed treatment plan? (medications, exercises, diet changes, etc.)
6. Any new or worsening symptoms since the visit
7. Do they need to schedule a follow-up appointment? (yes/no)
8. Any questions or concerns for their doctor

Guidelines:
- Be warm and caring — this is a wellness check, not an interrogation.
- Ask one or two questions at a time.
- If they report worsening symptoms or anything concerning (high fever, severe pain, difficulty breathing), advise them to call 911 or come in immediately — do NOT continue the follow-up.
- Once all information is collected, use the "save_followup" tool. Let them know the notes will be sent to their doctor and someone will reach out if a follow-up appointment is needed."""

FOLLOWUP_TOOL = {
    "type": "function",
    "function": {
        "name": "save_followup",
        "description": "Save the post-appointment follow-up notes after collecting all information.",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string", "description": "Patient's full name"},
                "appointment_date": {"type": "string", "description": "Date of the recent appointment"},
                "doctor_name": {"type": "string", "description": "Name of the doctor they saw"},
                "recovery_status": {
                    "type": "string",
                    "enum": ["better", "same", "worse"],
                    "description": "How the patient is feeling since the visit",
                },
                "following_treatment_plan": {"type": "string", "description": "Whether they are following the treatment plan and any details"},
                "new_symptoms": {"type": "string", "description": "Any new or worsening symptoms, or 'none'"},
                "needs_followup_appointment": {"type": "boolean", "description": "Whether the patient wants to schedule a follow-up"},
                "questions_for_doctor": {"type": "string", "description": "Any questions or concerns for their doctor, or 'none'"},
            },
            "required": [
                "full_name",
                "appointment_date",
                "doctor_name",
                "recovery_status",
                "following_treatment_plan",
                "new_symptoms",
                "needs_followup_appointment",
            ],
        },
    },
}


class AppointmentFollowupAgent(Agent):
    name = "appointment_followup"
    system_prompt = SYSTEM_PROMPT
    tools = [FOLLOWUP_TOOL]

    def handle_tool_call(self, name: str, args: dict) -> tuple[str, dict | None]:
        if name == "save_followup":
            record = {
                **args,
                "created_at": datetime.now().isoformat(),
            }
            logger.info(f"Follow-up saved: {json.dumps(record, indent=2)}")

            if args.get("recovery_status") == "worse":
                return (
                    "Follow-up notes saved. Patient reports worsening condition — flagged for urgent doctor review.",
                    args,
                )
            return (
                "Follow-up notes saved. The doctor will be notified and the clinic will reach out if further action is needed.",
                args,
            )
        return ("Unknown tool", None)
