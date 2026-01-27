from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Modulos do projeto
from video.inference_video import run_video_inference
from fusion.rules_engine import fuse_events
from alerts.alert_manager import save_alert_log


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _ensure_dirs() -> None:
    Path("results/logs").mkdir(parents=True, exist_ok=True)
    Path("results/video_outputs").mkdir(parents=True, exist_ok=True)
    Path("results/audio_outputs").mkdir(parents=True, exist_ok=True)


def _load_config() -> Dict[str, Any]:
    """
    Config simples via variáveis de ambiente por enquanto.
    Depois você pode migrar para config/thresholds.yaml e config/azure_config.yaml.
    """
    return {
        "VIDEO_INPUT": os.getenv("VIDEO_INPUT", "data/videos/sample.mp4"),
        "VIDEO_MODEL": os.getenv("VIDEO_MODEL", "yolov8n.pt"),
        "VIDEO_CONF": float(os.getenv("VIDEO_CONF", "0.35")),
        "OUTPUT_DIR": os.getenv("OUTPUT_DIR", "results"),
    }


def main() -> None:
    _ensure_dirs()
    cfg = _load_config()

    print("=== Tech Challenge Fase 4 | Pipeline Multimodal ===")
    print(f"[{_now_iso()}] Config: {json.dumps(cfg, ensure_ascii=False)}")

    # 1) Vídeo -> eventos visuais
    print("\n[1/4] Rodando análise de VÍDEO...")
    video_events = run_video_inference(
        video_path=cfg["VIDEO_INPUT"],
        model_path=cfg["VIDEO_MODEL"],
        conf_threshold=cfg["VIDEO_CONF"],
        output_dir=cfg["OUTPUT_DIR"],
    )
    print(f"Eventos de vídeo: {len(video_events)}")

    # 2) Áudio -> eventos vocais (placeholder por enquanto)
    # Nesta fase inicial, deixamos como lista vazia.
    print("\n[2/4] Rodando análise de ÁUDIO... (placeholder nesta etapa)")
    audio_events: List[Dict[str, Any]] = []

    # 3) Fusão multimodal -> alerta
    print("\n[3/4] Fundindo eventos e avaliando risco...")
    fusion_result = fuse_events(
        video_events=[asdict(e) for e in video_events],
        audio_events=audio_events,
    )
    print(f"Resultado de fusão: {json.dumps(fusion_result, ensure_ascii=False, indent=2)}")

    # 4) Persistência / log do alerta
    print("\n[4/4] Salvando log do alerta...")
    alert_path = save_alert_log(fusion_result, output_dir=cfg["OUTPUT_DIR"])
    print(f"Log salvo em: {alert_path}")

    print("\n✅ Pipeline concluído.")


if __name__ == "__main__":
    main()
