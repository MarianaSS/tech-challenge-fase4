from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class VideoEvent:
    type: str
    event: str
    confidence: float
    timestamp: str
    bbox: Optional[Tuple[float, float, float, float]] = None  # (x1, y1, x2, y2)
    label: Optional[str] = None
