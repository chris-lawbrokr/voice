import json
import logging
from datetime import datetime

from .base import Agent

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a warm, thorough intake coordinator for a multi-specialty medical group. Your job is to collect detailed information from the patient before their first visit.

Collect the following, one topic at a time — don't rush:
1. Full name
2. Date of birth
3. Insurance provider and member ID
4. Primary care physician (if they have one)
5. Chief complaint — what's bringing them in today
6. Symptom duration — when did it start, is it getting worse
7. Current medications (or "none")
8. Known allergies (or "none")
9. Preferred location (offer: Downtown, Westside, North Campus)
10. Preferred appointment date and time

Guidelines:
- Ask only 1-2 questions per turn to keep it conversational.
- If a patient seems unsure about insurance details, reassure them that the front desk can help verify later.
- If they mention anything that sounds urgent (chest pain, difficulty breathing, sudden vision loss), immediately tell them to call 911 or go to the nearest ER — do NOT continue intake.
- Once all fields are collected, use the "save_custom_intake" tool. Then confirm what you collected and let them know the clinic will reach out to finalize the appointment."""

CUSTOM_INTAKE_TOOL = {
    "type": "function",
    "function": {
        "name": "save_custom_intake",
        "description": "Save the detailed patient intake after all required fields are collected.",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string", "description": "Patient's full name"},
                "date_of_birth": {"type": "string", "description": "Patient's date of birth"},
                "insurance_provider": {"type": "string", "description": "Insurance company name"},
                "insurance_member_id": {"type": "string", "description": "Insurance member/policy ID"},
                "primary_care_physician": {"type": "string", "description": "Name of PCP or 'none'"},
                "chief_complaint": {"type": "string", "description": "Primary reason for the visit"},
                "symptom_duration": {"type": "string", "description": "How long symptoms have been present and trajectory"},
                "current_medications": {"type": "string", "description": "List of current medications or 'none'"},
                "known_allergies": {"type": "string", "description": "Known allergies or 'none'"},
                "preferred_location": {
                    "type": "string",
                    "enum": ["Downtown", "Westside", "North Campus"],
                    "description": "Preferred clinic location",
                },
                "preferred_appointment_time": {"type": "string", "description": "Preferred date and time"},
            },
            "required": [
                "full_name",
                "date_of_birth",
                "insurance_provider",
                "insurance_member_id",
                "chief_complaint",
                "symptom_duration",
                "current_medications",
                "known_allergies",
                "preferred_location",
                "preferred_appointment_time",
            ],
        },
    },
}


class CustomIntakeAgent(Agent):
    name = "custom_intake"
    system_prompt = SYSTEM_PROMPT
    tools = [CUSTOM_INTAKE_TOOL]

    def handle_tool_call(self, name: str, args: dict) -> tuple[str, dict | None]:
        if name == "save_custom_intake":
            record = {
                **args,
                "created_at": datetime.now().isoformat(),
            }
            logger.info(f"Custom intake saved: {json.dumps(record, indent=2)}")
            return (
                "Detailed intake saved successfully. The clinic will contact the patient to confirm the appointment.",
                args,
            )
        return ("Unknown tool", None)
