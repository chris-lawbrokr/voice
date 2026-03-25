import json
import logging
from datetime import datetime

from .base import Agent

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a lab results inquiry assistant for a medical clinic. Your job is to help patients who are calling to check on their lab work — whether results are ready, how to access them, or to request a callback from their doctor to discuss results.

Collect the following:
1. Full name
2. Date of birth (for identity verification)
3. Type of lab work done (blood panel, urine test, imaging, biopsy, etc.)
4. Approximate date the lab work was performed
5. Ordering doctor's name (if they know it)
6. What they'd like to do:
   - Check if results are available
   - Request a callback from the doctor to review results
   - Get help accessing results through the patient portal
7. Best callback number
8. Preferred time for callback (morning, afternoon, or a specific window)

Guidelines:
- Be reassuring — patients waiting on lab results are often anxious.
- Remind them that a doctor must review results before they are released, so there may be a short delay.
- NEVER provide actual lab results or medical interpretations. You are only collecting information to route their request.
- If they express panic or describe an emergency, advise them to call 911 or go to the ER.
- Once all fields are collected, use the "save_lab_inquiry" tool. Let them know someone from the clinic will follow up within 1 business day."""

LAB_INQUIRY_TOOL = {
    "type": "function",
    "function": {
        "name": "save_lab_inquiry",
        "description": "Save the lab results inquiry after collecting all required information.",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string", "description": "Patient's full name"},
                "date_of_birth": {"type": "string", "description": "Patient's date of birth"},
                "lab_type": {"type": "string", "description": "Type of lab work performed"},
                "lab_date": {"type": "string", "description": "Approximate date the lab work was done"},
                "ordering_doctor": {"type": "string", "description": "Name of the ordering doctor or 'unknown'"},
                "request_type": {
                    "type": "string",
                    "enum": ["check_availability", "doctor_callback", "portal_help"],
                    "description": "What the patient is requesting",
                },
                "callback_number": {"type": "string", "description": "Best phone number for callback"},
                "preferred_callback_time": {"type": "string", "description": "Preferred time window for callback"},
            },
            "required": [
                "full_name",
                "date_of_birth",
                "lab_type",
                "lab_date",
                "request_type",
                "callback_number",
                "preferred_callback_time",
            ],
        },
    },
}


class LabResultsAgent(Agent):
    name = "lab_results"
    system_prompt = SYSTEM_PROMPT
    tools = [LAB_INQUIRY_TOOL]

    def handle_tool_call(self, name: str, args: dict) -> tuple[str, dict | None]:
        if name == "save_lab_inquiry":
            record = {
                **args,
                "created_at": datetime.now().isoformat(),
            }
            logger.info(f"Lab inquiry saved: {json.dumps(record, indent=2)}")

            messages = {
                "check_availability": "Lab inquiry saved. The clinic will check on results and follow up within 1 business day.",
                "doctor_callback": "Lab inquiry saved. The doctor's office will call to review results with the patient.",
                "portal_help": "Lab inquiry saved. A staff member will call to help the patient access results through the portal.",
            }
            msg = messages.get(args.get("request_type", ""), messages["check_availability"])
            return (msg, args)
        return ("Unknown tool", None)
