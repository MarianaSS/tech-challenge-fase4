from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Modulos do projeto
from video.inference_video import run_video_inference
from fusion.rules_engine import fuse_events
from alerts.alert_manager import save_alert_log

from audio.audio_features import extract_audio_features
from audio.urgency_detection import detect_clinical_urgency

from azure_integration.function_client import send_alert_to_function

def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _ensure_dirs() -> None:
    Path("results/logs").mkdir(parents=True, exist_ok=True)
    Path("results/video_outputs").mkdir(parents=True, exist_ok=True)
    Path("results/audio_outputs").mkdir(parents=True, exist_ok=True)


def _load_config() -> Dict[str, Any]:
    return {
        "VIDEO_INPUT": os.getenv("VIDEO_INPUT", "data/videos/pph_simulation_clip.mp4"),
        "FULL_VIDEO_INPUT": os.getenv("FULL_VIDEO_INPUT", "data/videos/full_pph_video.mp4"),
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

    # 2) Áudio -> eventos vocais
    print("\n[2/4] Rodando análise de ÁUDIO...")
    audio_features = extract_audio_features(
        audio_path="data/audios/patient_distress_audio.wav",
        language="en-US",
    )
    audio_events = detect_clinical_urgency(audio_features)

    print("Transcrição:", audio_features.get("transcript", "")[:300])
    print("Audio dBFS:", audio_features.get("audio_dbfs"))
    print("Chunks:", audio_features.get("num_chunks"))
    print("Chunks transcript:", audio_features.get("chunks_transcript", [])[:3])


    audio_events = detect_clinical_urgency(audio_features)
    print(f"Eventos de áudio: {len(audio_events)}")

    # 3) Fusão multimodal -> alerta
    print("\n[3/4] Fundindo eventos e avaliando risco...")
    fusion_result = fuse_events(
        video_events=[asdict(e) for e in video_events],
        audio_events=[asdict(e) for e in audio_events],
    )

    print(f"Resultado de fusão: {json.dumps(fusion_result, ensure_ascii=False, indent=2)}")

    # 4) Persistência / log do alerta
    print("\n[4/4] Salvando log do alerta...")
    alert_path = save_alert_log(fusion_result, output_dir=cfg["OUTPUT_DIR"])
    print(f"Log salvo em: {alert_path}")

    print("\n✅ Pipeline concluído.")

    # 5) Enviar alerta para Azure Function
    azure_payload = {
        "risk_level": fusion_result.get("risk_level"),
        "reasons": fusion_result.get("reasons", []),
        "action": fusion_result.get("action"),
        "video_summary": {"count_events": len(video_events)},
        "audio_summary": {"count_events": len(audio_events)},
        "transcript": audio_features.get("transcript", "")[:500],
    }

    azure_resp = send_alert_to_function(azure_payload)
    print("Azure response:", azure_resp)

if __name__ == "__main__":
    main()
