from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def save_alert_log(alert: Dict[str, Any], output_dir: str = "results") -> str:
    Path(f"{output_dir}/logs").mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = Path(output_dir) / "logs" / f"alert_{ts}.json"

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(alert, f, ensure_ascii=False, indent=2)

    return str(out_path)
