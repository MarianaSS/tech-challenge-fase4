from __future__ import annotations

from typing import Any, Dict, List


def fuse_events(video_events: List[Dict[str, Any]], audio_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Motor simples de regras multimodais.
    Nesta versão: se houver evento de sangramento + evento de dor vocal, risco HIGH.
    """
    has_bleeding = any(e.get("event") == "anomalous_bleeding" and e.get("confidence", 0) >= 0.5 for e in video_events)
    has_pain = any(e.get("event") == "possible_pain_vocalization" and e.get("confidence", 0) >= 0.5 for e in audio_events)

    if has_bleeding and has_pain:
        return {
            "risk_level": "high",
            "reasons": ["bleeding", "pain_vocalization"],
            "action": "notify_medical_team",
        }

    if has_bleeding:
        return {
            "risk_level": "medium",
            "reasons": ["bleeding"],
            "action": "review_procedure",
        }

    if has_pain:
        return {
            "risk_level": "medium",
            "reasons": ["pain_vocalization"],
            "action": "check_patient_comfort",
        }

    return {
        "risk_level": "low",
        "reasons": [],
        "action": "no_action",
    }
