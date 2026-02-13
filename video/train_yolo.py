from ultralytics import YOLO

DATASET_YAML = "data/dataset/dataset.yaml"

def main():
    # Carrega o modelo base
    model = YOLO("yolov8n.pt")

    # Treino
    model.train(
        data=DATASET_YAML,
        epochs=25,
        imgsz=640,
        batch=8,
        device="mps",      # Apple Silicon acceleration
        project="results/yolo_runs",
        name="bleeding_yolov8n",
        verbose=True,
    )

if __name__ == "__main__":
    main()
