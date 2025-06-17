from pynput import keyboard, mouse
from threading import Thread
import time
import cv2
from ultralytics import YOLO

# ------------------------ Global State Control ------------------------
last_input_time = time.time()
IDLE_THRESHOLD = 10  # For testing; set back to 180 for deployment
yolo_running = False

# ------------------------ Utility Functions ------------------------
def compute_overlap_area(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    return max(0, x2 - x1) * max(0, y2 - y1)

def compute_area(box):
    return (box[2] - box[0]) * (box[3] - box[1])

def extract_detections(results, model):
    detections = {}
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            xyxy = box.xyxy[0].cpu().numpy()
            detections.setdefault(label, []).append(xyxy)
    return detections

# ------------------------ Main Detection Logic ------------------------
def yolo_loop():
    global yolo_running
    model = YOLO("yolo11n.pt")
    cap = cv2.VideoCapture(0)

    print("🟡 YOLO started: monitoring for person + phone/remote (3 min)")
    start_time = time.time()
    person_detected = False

    def handle_prohibited_behavior(label):
        print(f"\n🚨 Prohibited item [{label}] detected — triggering control action")
        # Replace this with system lock, sound alert, etc.
        cap.release()
        cv2.destroyAllWindows()
        exit(0)

    while yolo_running and (time.time() - start_time < 180):
        ret, frame = cap.read()
        if not ret:
            continue

        results = model(frame, verbose=False)  # suppress internal logging
        detections = extract_detections(results, model)

        # Visualization — comment out if not needed
        annotated_frame = results[0].plot()
        cv2.imshow("YOLO Live View", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🔴 YOLO manually interrupted")
            break

        # Step 1: Check if person is present
        if not person_detected:
            if "person" in detections:
                person_detected = True
                print(f"\n✅ Person detected — starting behavior monitoring phase")
            else:
                time.sleep(3)
                continue

        # Step 2: Detect specific items
        for label in ["cell phone", "remote"]:
            if label in detections:
                print(f"\n📸 Person present + [{label}] detected → intervention triggered")
                handle_prohibited_behavior(label)
                return

        time.sleep(3)

    cap.release()
    cv2.destroyAllWindows()
    yolo_running = False

    if person_detected:
        print("\n🟢 Person detected within 3 minutes, but no prohibited items found")
    else:
        print("\n⚪ No person detected within 3 minutes")

# ------------------------ Input Listener ------------------------
def on_input(_):
    global last_input_time, yolo_running
    last_input_time = time.time()
    if yolo_running:
        print("\n🛑 Input received — stopping YOLO monitoring")
        yolo_running = False

# ------------------------ Idle Monitor Dispatcher ------------------------
def monitor_loop():
    global yolo_running
    while True:
        idle_time = time.time() - last_input_time
        print(f"⌛ Idle time: {idle_time:.1f}s", end='\r')
        if idle_time > IDLE_THRESHOLD and not yolo_running:
            yolo_running = True
            Thread(target=yolo_loop).start()
        time.sleep(1)

# ------------------------ Program Entry ------------------------
keyboard.Listener(on_press=on_input).start()
mouse.Listener(on_click=on_input, on_move=on_input, on_scroll=on_input).start()

monitor_loop()
