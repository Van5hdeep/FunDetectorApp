import argparse
import sys
import time
from typing import Optional

import cv2

def _play_windows_alert_once() -> None:
    """
    Play the built-in Windows alert sound asynchronously.
    """
    if not sys.platform.startswith("win"):
        return
    try:
        import winsound

        winsound.MessageBeep(winsound.MB_ICONHAND)
    except Exception:
        pass


def _load_model(model_path: str):
    try:
        from ultralytics import YOLO
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "ultralytics is not installed. Install it with: pip install ultralytics"
        ) from e

    try:
        return YOLO(model_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"YOLO model file not found: {model_path}\n"
            "Tip: use 'yolov8n.pt' (auto-downloads on first run if internet is available), "
            "or place the model file next to this script and pass its filename."
        ) from e
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"Failed to load YOLO model '{model_path}': {e}") from e


def _open_camera(camera_index: int):
    """
    Try multiple OpenCV backends on Windows for better compatibility.
    """
    attempted = []

    if sys.platform.startswith("win"):
        # DSHOW often fixes MSMF read errors on some Windows drivers.
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        attempted.append("CAP_DSHOW")
        if cap.isOpened():
            return cap, attempted
        cap.release()

        cap = cv2.VideoCapture(camera_index, cv2.CAP_MSMF)
        attempted.append("CAP_MSMF")
        if cap.isOpened():
            return cap, attempted
        cap.release()

    # Default backend attempt.
    cap = cv2.VideoCapture(camera_index)
    attempted.append("default")
    if cap.isOpened():
        return cap, attempted
    cap.release()

    return None, attempted


def _parse_args():
    parser = argparse.ArgumentParser(description="Real-time phone detection with YOLOv8.")
    parser.add_argument("--model", default="yolov8n.pt", help="YOLO model path/name.")
    parser.add_argument("--camera", type=int, default=0, help="Webcam index.")
    parser.add_argument("--width", type=int, default=640, help="Frame width.")
    parser.add_argument("--height", type=int, default=480, help="Frame height.")
    parser.add_argument("--conf", type=float, default=0.35, help="Detection confidence threshold.")
    return parser.parse_args()


def main(
    model_path: str = "yolov8n.pt",
    camera_index: int = 0,
    width: int = 640,
    height: int = 480,
    conf: float = 0.35,
) -> int:
    # Load YOLO model.
    try:
        model = _load_model(model_path)
    except Exception as e:
        print(f"[ERROR] {e}")
        return 3

    # Open webcam.
    cap, attempted_backends = _open_camera(camera_index)
    if cap is None:
        print(
            "[ERROR] Could not access webcam.\n"
            f"Tried backends: {', '.join(attempted_backends)}\n"
            f"Try a different camera index (current: {camera_index}) or close other camera apps."
        )
        return 4

    try:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        phone_present_prev = False
        last_infer_time_s: Optional[float] = None

        while True:
            ok, frame = cap.read()
            if not ok or frame is None:
                print("[ERROR] Failed to read frame from webcam.")
                break

            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)

            # Inference.
            t0 = time.time()
            try:
                results = model.predict(frame, verbose=False, conf=conf)
            except Exception as e:
                print(f"[ERROR] YOLO inference failed: {e}")
                break
            t1 = time.time()
            last_infer_time_s = t1 - t0

            phone_present_now = False

            # YOLOv8 results list (one item for one frame).
            r = results[0]
            names = getattr(r, "names", None) or getattr(model, "names", {})

            boxes = getattr(r, "boxes", None)
            if boxes is not None and getattr(boxes, "xyxy", None) is not None:
                xyxy = boxes.xyxy.cpu().numpy()
                cls = boxes.cls.cpu().numpy().astype(int) if getattr(boxes, "cls", None) is not None else []
                confs = (
                    boxes.conf.cpu().numpy()
                    if getattr(boxes, "conf", None) is not None
                    else [None] * len(xyxy)
                )

                for i in range(len(xyxy)):
                    class_id = int(cls[i]) if len(cls) > i else -1
                    class_name = names.get(class_id, str(class_id))

                    if class_name == "cell phone":
                        phone_present_now = True
                        x1, y1, x2, y2 = map(int, xyxy[i])

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        label = "Phone"
                        if confs is not None and len(confs) > i and confs[i] is not None:
                            label = f"Phone {float(confs[i]):.2f}"
                        cv2.putText(
                            frame,
                            label,
                            (x1, max(0, y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 255),
                            2,
                            cv2.LINE_AA,
                        )

            # Trigger sound only when detection starts.
            if phone_present_now and not phone_present_prev:
                _play_windows_alert_once()
            phone_present_prev = phone_present_now

            # Overlay performance info.
            if last_infer_time_s is not None:
                fps = 1.0 / max(last_infer_time_s, 1e-6)
                cv2.putText(
                    frame,
                    f"YOLO FPS: {fps:.1f}",
                    (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow("Phone Detection (ESC to exit)", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    args = _parse_args()
    raise SystemExit(
        main(
            model_path=args.model,
            camera_index=args.camera,
            width=args.width,
            height=args.height,
            conf=args.conf,
        )
    )

