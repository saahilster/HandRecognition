import mediapipe as mp
from pathlib import Path
import WindowLogic as wl
import cv2
import time

doom = wl.Scroller(interval=3, key="down")   # duration removed

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

timelapse = 0

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

p = Path(r"C:/Users/faroo\Desktop/Python/HandTrackingTest/gesture_recognizer.task")
with p.open("rb") as f:
    buf = f.read()

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    # Guard against empty results
    if not result.gestures:
        return
    for i in result.gestures:
        signal = i[-1].category_name
        if signal == "Closed_Fist":
            wl.minimize()
            print(signal)
        elif signal == "Open_Palm":
            wl.maximize()
            print(signal)
        elif signal == "Thumb_Up":
            # small debounce
            time.sleep(0.1)
            print("Turned On")
            doom.start()
        elif signal == "Thumb_Down":
            print("Turn Off")
            time.sleep(0.1)
            doom.stop()
        elif signal == "Victory":
            print("Peace")
            wl.StopProgram()

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_buffer=buf),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=1,
    result_callback=print_result
)

with GestureRecognizer.create_from_options(options) as recognizer:
    while True:
        timelapse += 1
        success, frame = cap.read()
        if not success:
            continue

        srgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=srgb_frame)
        recognizer.recognize_async(mp_image, timelapse)

        result = hands.process(srgb_frame)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # >>> IMPORTANT: tick the scroller every frame (no threads needed)
        doom.update()

        cv2.imshow("capture image", frame)
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()
