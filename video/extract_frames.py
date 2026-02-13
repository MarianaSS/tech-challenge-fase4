import cv2
from pathlib import Path

VIDEO_PATH = "data/videos/pph_simulation_clip.mp4"
OUT_DIR = Path("data/frames")
FRAME_EVERY = 10  # pega 1 frame a cada 10

OUT_DIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS) or 30

idx = 0
saved = 0

while True:
    ok, frame = cap.read()
    if not ok:
        break

    if idx % FRAME_EVERY == 0:
        out = OUT_DIR / f"frame_{saved:04d}.jpg"
        cv2.imwrite(str(out), frame)
        saved += 1

    idx += 1

cap.release()
print(f"Frames salvos: {saved}")
