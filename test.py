from ultralytics import YOLO

model: YOLO = YOLO("train\\weights\\windows_best.pt")
model.export(format='engine', half=True)
