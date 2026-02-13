import cv2
import numpy as np
from pathlib import Path

FRAMES_DIR = Path("data/frames")
IMG_TRAIN = Path("data/dataset/images/train")
LBL_TRAIN = Path("data/dataset/labels/train")

IMG_TRAIN.mkdir(parents=True, exist_ok=True)
LBL_TRAIN.mkdir(parents=True, exist_ok=True)

BLEEDING_CLASS_ID = 0  # única classe: bleeding

for img_path in FRAMES_DIR.glob("*.jpg"):
    img = cv2.imread(str(img_path))
    if img is None:
        continue

    h, w, _ = img.shape

    # Converte para HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Faixas de vermelho em HSV (duas bandas)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 | mask2

    # Limpeza morfológica
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    label_lines = []

    for cnt in contours:
        x, y, bw, bh = cv2.boundingRect(cnt)

        # filtra ruído pequeno
        if bw * bh < 0.002 * (w * h):
            continue

        # YOLO format: class cx cy w h (normalizado)
        cx = (x + bw / 2) / w
        cy = (y + bh / 2) / h
        nw = bw / w
        nh = bh / h

        label_lines.append(
            f"{BLEEDING_CLASS_ID} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}"
        )

    # salva imagem
    out_img = IMG_TRAIN / img_path.name
    cv2.imwrite(str(out_img), img)

    # salva label (mesmo vazio, YOLO aceita)
    out_lbl = LBL_TRAIN / f"{img_path.stem}.txt"
    with out_lbl.open("w") as f:
        f.write("\n".join(label_lines))

print("Labels de sangramento geradas automaticamente.")
