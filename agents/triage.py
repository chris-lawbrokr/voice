import json
import logging
from datetime import datetime

from .base import Agent

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a medical triage assistant for a clinic. Your job is to assess the caller's symptoms and determine the urgency level and appropriate department.

Ask about:
1. Their primary symptoms and when they started
2. Severity on a scale of 1-10
3. Any related symptoms (fever, nausea, dizziness, etc.)
4. Relevant medical history or current medications
5. Whether symptoms are getting better, worse, or staying the same

Based on the information, use the "save_triage" tool to record your assessment. Urgency levels:
- "emergency": Life-threatening — tell them to call 911 or go to the ER immediately
- "urgent": Needs to be seen within 24 hours
- "soon": Should be seen within a few days
- "routine": Can be scheduled at their convenience

Be calm, empathetic, and clear. If anything sounds life-threatening at any point, immediately advise them to call 911 before continuing."""

TRIAGE_TOOL = {
    "type": "function",
    "function": {
        "name": "save_triage",
        "description": "Save the triage assessment after evaluating the caller's symptoms.",
        "parameters": {
            "type": "object",
            "properties": {
                "symptoms": {"type": "string", "description": "Summary of reported symptoms"},
                "severity": {"type": "integer", "description": "Patient-reported severity 1-10"},
                "urgency": {
                    "type": "string",
                    "enum": ["emergency", "urgent", "soon", "routine"],
                    "description": "Assessed urgency level",
                },
                "department": {
                    "type": "string",
                    "description": "Recommended department (e.g. General Practice, Cardiology, Orthopedics, Dermatology, Neurology, Gastroenterology, ENT, Urgent Care)",
                },
                "notes": {"type": "string", "description": "Additional clinical notes or recommendations"},
            },
            "required": ["symptoms", "severity", "urgency", "department", "notes"],
        },
    },
}

URGENCY_RESPONSES = {
    "emergency": "Triage recorded. EMERGENCY — patient advised to call 911 immediately.",
    "urgent": "Triage recorded. Patient flagged for urgent callback within 24 hours.",
    "soon": "Triage recorded. Patient should be seen within a few days.",
    "routine": "Triage recorded. Patient can schedule a routine appointment at their convenience.",
}


class TriageAgent(Agent):
    name = "triage"
    system_prompt = SYSTEM_PROMPT
    tools = [TRIAGE_TOOL]

    def handle_tool_call(self, name: str, args: dict) -> tuple[str, dict | None]:
        if name == "save_triage":
            triage = {
                **args,
                "created_at": datetime.now().isoformat(),
            }
            logger.info(f"Triage saved: {json.dumps(triage, indent=2)}")
            response = URGENCY_RESPONSES.get(args.get("urgency", "routine"), URGENCY_RESPONSES["routine"])
            return (response, args)
        return ("Unknown tool", None)
