from ultralytics import YOLO

class Tracker:
    def __init__(self, model_version):
        self.model = YOLO(model_version)

    def detect_players(self, frame):
        results = self.model.predict(frame, conf=0.1)

        # Get image(s) with detections drawn
        detected_images = [r.plot() for r in results]

        # Return the first image (or modify if batching is needed)
        return detected_images[0] if detected_images else frame
