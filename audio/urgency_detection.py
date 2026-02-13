from __future__ import annotations

from typing import Dict, Any, List

from audio.audio_events import AudioEvent


DISTRESS_PATTERNS = [
    "i don't feel good",
    "dont feel good",
    "i feel dizzy",
    "dizzy",
    "hurts",
]


def detect_clinical_urgency(audio_features: Dict[str, Any]) -> List[AudioEvent]:
    """
    Mantém o nome 'detect_clinical_urgency' para compatibilidade com seu pipeline,
    mas na prática detecta distress/mal-estar relatado pela paciente via transcrição.
    """
    transcript = (audio_features.get("transcript") or "").lower()
    hits = [p for p in DISTRESS_PATTERNS if p in transcript]

    if not hits:
        return []

    confidence = min(1.0, 0.7 + 0.1 * len(hits))

    return [
        AudioEvent(
            type="audio_event",
            event="patient_distress_detected",
            confidence=confidence,
            timestamp="N/A",  # SpeechRecognition básico não fornece timestamps
            details={
                "hits": hits,
                "transcript": audio_features.get("transcript", ""),
                "wav_path": audio_features.get("wav_path", ""),
            },
        )
    ]
