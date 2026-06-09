"""Assessment schema and model-output normalization."""

from __future__ import annotations

from typing import Any

RISK_LABELS = (
    "Looks normal",
    "Verify first",
    "Suspicious",
    "Likely scam",
    "Inappropriate",
)
REQUIRED_FIELDS = {
    "risk_label",
    "simple_explanation",
    "red_flags",
    "safe_next_steps",
    "reply_draft",
}
OUTPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "risk_label": {"type": "string", "enum": list(RISK_LABELS)},
        "simple_explanation": {"type": "string"},
        "red_flags": {"type": "array", "items": {"type": "string"}},
        "safe_next_steps": {"type": "array", "items": {"type": "string"}},
        "reply_draft": {"type": "string"},
    },
    "required": sorted(REQUIRED_FIELDS),
    "additionalProperties": False,
}


def normalize_assessment(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Model response must be a JSON object.")
    missing = REQUIRED_FIELDS - value.keys()
    if missing:
        raise ValueError("Model response is missing: " + ", ".join(sorted(missing)))

    label_map = {
        "low": "Looks normal",
        "medium": "Verify first",
        "high": "Likely scam",
    }
    label = label_map.get(str(value["risk_label"]).strip().lower(), value["risk_label"])
    if label not in RISK_LABELS:
        raise ValueError("Model returned an unsupported risk label.")

    result = {
        "risk_label": label,
        "simple_explanation": str(value["simple_explanation"]).strip(),
        "red_flags": value["red_flags"],
        "safe_next_steps": value["safe_next_steps"],
        "reply_draft": (
            str(value["reply_draft"]).strip()
            if label in {"Verify first", "Suspicious"}
            else ""
        ),
    }
    if not result["simple_explanation"]:
        raise ValueError("simple_explanation must not be empty.")
    for field in ("red_flags", "safe_next_steps"):
        items = result[field]
        if not isinstance(items, list):
            raise ValueError(f"{field} must be an array.")
        result[field] = [str(item).strip() for item in items if str(item).strip()]

    if not result["red_flags"]:
        result["red_flags"] = ["No specific red flags identified."]
    if not result["safe_next_steps"]:
        result["safe_next_steps"] = [
            "Verify the message through official channels independently.",
            "Do not share personal information or click links until verified.",
        ]
    return result
