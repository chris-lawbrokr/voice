import json
import logging
from datetime import datetime

from .base import Agent

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful prescription refill assistant for a medical clinic. Your job is to collect the information needed to process a medication refill request.

Collect the following:
1. Full name
2. Date of birth (for identity verification)
3. Medication name
4. Medication dosage (e.g. 10mg, 20mg)
5. Pharmacy name and location (or "same pharmacy on file")
6. Number of refills requested
7. Are they experiencing any new side effects or issues with the medication? (yes/no, and details if yes)
8. Prescribing doctor's name (if they know it)

Guidelines:
- Be friendly but efficient — patients calling for refills usually want it done quickly.
- If they mention new or worsening side effects, note it clearly and let them know the doctor will review before approving.
- If they describe anything that sounds like a serious reaction (difficulty breathing, swelling, chest pain), tell them to stop taking the medication and call 911 or go to the ER immediately.
- Once all fields are collected, use the "save_refill_request" tool. Then let them know the request has been submitted and the pharmacy will be notified once the doctor approves, typically within 24-48 hours."""

REFILL_TOOL = {
    "type": "function",
    "function": {
        "name": "save_refill_request",
        "description": "Save the prescription refill request after collecting all required information.",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string", "description": "Patient's full name"},
                "date_of_birth": {"type": "string", "description": "Patient's date of birth"},
                "medication_name": {"type": "string", "description": "Name of the medication to refill"},
                "dosage": {"type": "string", "description": "Medication dosage"},
                "pharmacy": {"type": "string", "description": "Pharmacy name and location"},
                "num_refills": {"type": "integer", "description": "Number of refills requested"},
                "side_effects": {"type": "string", "description": "Any new side effects or 'none'"},
                "prescribing_doctor": {"type": "string", "description": "Name of prescribing doctor or 'unknown'"},
            },
            "required": [
                "full_name",
                "date_of_birth",
                "medication_name",
                "dosage",
                "pharmacy",
                "num_refills",
                "side_effects",
            ],
        },
    },
}


class PrescriptionRefillAgent(Agent):
    name = "prescription_refill"
    system_prompt = SYSTEM_PROMPT
    tools = [REFILL_TOOL]

    def handle_tool_call(self, name: str, args: dict) -> tuple[str, dict | None]:
        if name == "save_refill_request":
            record = {
                **args,
                "status": "pending_review" if args.get("side_effects", "none").lower() != "none" else "pending_approval",
                "created_at": datetime.now().isoformat(),
            }
            logger.info(f"Refill request saved: {json.dumps(record, indent=2)}")
            status_msg = (
                "Refill request saved. Due to reported side effects, the doctor will review before approving."
                if record["status"] == "pending_review"
                else "Refill request saved. The pharmacy will be notified once the doctor approves, typically within 24-48 hours."
            )
            return (status_msg, args)
        return ("Unknown tool", None)
