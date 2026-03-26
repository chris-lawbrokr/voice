import json
import logging
from datetime import datetime

from .base import Agent

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful prescription refill assistant for a medical clinic. Your job is to help callers request refills on their existing prescriptions.

You must collect the following information:
1. Full name (as it appears on their prescription)
2. Date of birth (for identity verification)
3. Prescription medication name and dosage
4. Prescription number (found on the label, if available)
5. Pharmacy name and location where they'd like the refill sent
6. Whether they need any other medications refilled at the same time

Guidelines:
- Verify the caller's identity before processing any refill.
- If the caller doesn't have their prescription number, reassure them you can look it up by name and medication.
- Remind callers that controlled substances (Schedule II-V) may require a new prescription from their provider and cannot be refilled through this system.
- If the prescription might be expired (over 12 months), let them know their provider may need to authorize a new one.
- After collecting all information, use the "save_refill_request" tool to save the request.
- Be friendly, patient, and HIPAA-conscious — never read back full date of birth or prescription details unprompted.

Thank the caller and let them know their refill will typically be ready within 24-48 hours, and the pharmacy will notify them."""

REFILL_REQUEST_TOOL = {
    "type": "function",
    "function": {
        "name": "save_refill_request",
        "description": "Save a prescription refill request after collecting all required information from the caller.",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string", "description": "Patient's full name as on prescription"},
                "date_of_birth": {"type": "string", "description": "Patient's date of birth for verification"},
                "medication_name": {"type": "string", "description": "Name of the medication to refill"},
                "dosage": {"type": "string", "description": "Dosage of the medication (e.g. 10mg, 500mg)"},
                "prescription_number": {"type": "string", "description": "Prescription/Rx number from the label, if available"},
                "pharmacy_name": {"type": "string", "description": "Name of the pharmacy for the refill"},
                "pharmacy_location": {"type": "string", "description": "Location/address of the pharmacy"},
                "additional_medications": {
                    "type": "string",
                    "description": "Any other medications to refill at the same time, or 'none'",
                },
            },
            "required": ["full_name", "date_of_birth", "medication_name", "dosage", "pharmacy_name"],
        },
    },
}

CHECK_CONTROLLED_SUBSTANCE_TOOL = {
    "type": "function",
    "function": {
        "name": "check_controlled_substance",
        "description": "Check whether a medication is a controlled substance. Call this before saving a refill request to determine if the medication can be refilled or requires a new prescription.",
        "parameters": {
            "type": "object",
            "properties": {
                "medication_name": {"type": "string", "description": "Name of the medication to check"},
            },
            "required": ["medication_name"],
        },
    },
}
