from __future__ import annotations

from pathlib import Path
from typing import List

from video.video_events import VideoEvent


def run_video_inference(
    video_path: str,
    model_path: str,
    conf_threshold: float,
    output_dir: str = "results",
) -> List[VideoEvent]:
    """
    Placeholder inicial: retorna 0 eventos.
    Na Semana 2, vamos implementar com YOLOv8 (ultralytics) e:
      - rodar inferência no vídeo
      - salvar vídeo anotado em results/video_outputs/
      - gerar lista de VideoEvent
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # TODO: implementar com YOLOv8
    return []
