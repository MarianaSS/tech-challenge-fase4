from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AudioEvent:
    type: str
    event: str
    confidence: float
    timestamp: str
    details: Optional[Dict[str, Any]] = None
