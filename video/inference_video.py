from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import torch
from ultralytics import YOLO

from video.video_events import VideoEvent


def _pick_device() -> str:
    # macOS Apple Silicon: MPS
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    # CUDA
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def _format_ts(seconds: float) -> str:
    m = int(seconds // 60)
    s = seconds - (m * 60)
    return f"{m:02d}:{s:06.3f}"


def _draw_box(
    frame,
    bbox: Tuple[float, float, float, float],
    label: str,
    conf: float,
) -> None:
    x1, y1, x2, y2 = map(int, bbox)

    # retângulo
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # texto
    text = f"{label} {conf:.2f}"
    (tw, th), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(frame, (x1, y1 - th - baseline - 6), (x1 + tw + 6, y1), (0, 0, 255), -1)
    cv2.putText(frame, text, (x1 + 3, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def run_video_inference(
    video_path: str,
    model_path: str,
    conf_threshold: float,
    output_dir: str = "results",
    target_label: str = "anomalous_bleeding",
    min_conf: float = 0.60,
    min_bbox_area_ratio: float = 0.015,  # 1.5% do frame
) -> List[VideoEvent]:
    """
    Roda YOLOv8 em um vídeo e retorna eventos detectados.
    Gera vídeo anotado APENAS com as boxes filtradas (classe + conf + área).

    Saída: results/video_outputs/annotated_<nome>.mp4
    """
    output_base = Path(output_dir)
    out_dir = output_base / "video_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    video_file = Path(video_path)
    if not video_file.exists():
        raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")

    device = _pick_device()
    model = YOLO(model_path)

    cap = cv2.VideoCapture(str(video_file))
    if not cap.isOpened():
        raise RuntimeError(f"Não consegui abrir o vídeo: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 1280)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 720)

    out_path = out_dir / f"annotated_{video_file.stem}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_path), fourcc, fps, (w, h))

    events: List[VideoEvent] = []
    frame_idx = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            # Inferência no frame
            results = model.predict(
                source=frame,
                conf=conf_threshold,
                device=device,
                verbose=False,
            )

            r0 = results[0]
            boxes = getattr(r0, "boxes", None)

            # tempo do frame
            ts_seconds = frame_idx / fps
            ts = _format_ts(ts_seconds)

            # Vamos desenhar em uma cópia do frame original
            annotated = frame.copy()

            if boxes is not None and boxes.xyxy is not None and len(boxes) > 0:
                for i in range(len(boxes)):
                    conf = float(boxes.conf[i].item()) if boxes.conf is not None else 0.0
                    cls_id = int(boxes.cls[i].item()) if boxes.cls is not None else -1
                    xyxy = boxes.xyxy[i].tolist()  # [x1, y1, x2, y2]

                    # Nome da classe
                    label_name: Optional[str] = None
                    if hasattr(model, "names") and isinstance(model.names, dict):
                        label_name = model.names.get(cls_id)

                    # 1) filtrar por classe (nosso dataset tem "bleeding")
                    if label_name is not None and label_name != "bleeding":
                        continue

                    # 2) filtrar por confiança
                    if conf < min_conf:
                        continue

                    # 3) filtrar por área relativa
                    x1, y1, x2, y2 = map(float, xyxy)
                    bbox_w = max(0.0, x2 - x1)
                    bbox_h = max(0.0, y2 - y1)
                    bbox_area_ratio = (bbox_w * bbox_h) / float(w * h)
                    if bbox_area_ratio < min_bbox_area_ratio:
                        continue

                    bbox = (x1, y1, x2, y2)

                    # desenha só as boxes filtradas
                    _draw_box(
                        annotated,
                        bbox=bbox,
                        label="bleeding",
                        conf=conf,
                    )

                    # salva evento (também só os filtrados)
                    events.append(
                        VideoEvent(
                            type="video_event",
                            event=target_label,  # "anomalous_bleeding"
                            confidence=conf,
                            timestamp=ts,
                            bbox=bbox,
                            label=label_name,
                        )
                    )

            # garantir tamanho
            if annotated.shape[1] != w or annotated.shape[0] != h:
                annotated = cv2.resize(annotated, (w, h))

            writer.write(annotated)
            frame_idx += 1

    finally:
        cap.release()
        writer.release()

    return events
