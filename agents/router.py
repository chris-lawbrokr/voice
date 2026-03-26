from fastapi import APIRouter, Request

from .base import Agent
from .appointment_followup import AppointmentFollowupAgent
from .custom_intake import CustomIntakeAgent
from .intake import IntakeAgent
from .lab_results import LabResultsAgent
from .prescription_refill import PrescriptionRefillAgent
from .triage import TriageAgent

router = APIRouter(prefix="/agents", tags=["agents"])

REGISTRY: dict[str, Agent] = {
    "intake": IntakeAgent(),
    "triage": TriageAgent(),
    "custom_intake": CustomIntakeAgent(),
    "appointment_followup": AppointmentFollowupAgent(),
    "lab_results": LabResultsAgent(),
    "prescription_refill": PrescriptionRefillAgent(),
}


@router.get("/")
async def list_agents():
    return {"agents": list(REGISTRY.keys())}


@router.post("/{agent_name}/chat")
async def agent_chat(agent_name: str, request: Request):
    if agent_name not in REGISTRY:
        return {"error": f"Unknown agent '{agent_name}'. Available: {list(REGISTRY.keys())}"}

    body = await request.json()
    user_message = body.get("message", "")
    session_id = body.get("session_id")

    agent = REGISTRY[agent_name]
    return agent.chat(user_message, session_id)


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    Agent.delete_session(session_id)
    return {"status": "deleted"}
