from typing import List, Dict
from audio.audio_events import AudioEvent

DISTRESS_PATTERNS = [
    "i don't feel good",
    "dont feel good",
    "i feel dizzy",
    "dizzy",
    "deezy",
    "lightheaded",
    "faint",
    "i feel sick",
    "nauseous",
]

def detect_patient_distress_from_text(text: str) -> List[AudioEvent]:
    text_l = (text or "").lower()
    hits = [p for p in DISTRESS_PATTERNS if p in text_l]

    if not hits:
        return []

    confidence = min(1.0, 0.7 + 0.1 * len(hits))
    return [
        AudioEvent(
            type="audio_event",
            event="patient_distress_detected",
            confidence=confidence,
            timestamp="N/A",  # SpeechRecognition básico não dá timestamp
            details={"hits": hits, "text": text},
        )
    ]
