import cv2
import mediapipe as mp
import math
import pyautogui
from Dependencies import *
import time

# -------------------------------
# Setup MediaPipe Hands & PyAutoGUI
# -------------------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

screen_w, screen_h = pyautogui.size()

# Track if mouse buttons are currently held
holding_left = False
holding_right = False

#Setup Smoothing
prev_x, prev_y = 0, 0
smooth_factor = 0.4  # smaller = smoother, larger = more responsive

#Disable fail-safe (makes movement not work as well)
pyautogui.FAILSAFE = False
# -------------------------------
# Start hand detection
# -------------------------------
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    # Initial line colors
    colorTI = (255, 255, 255)
    colorTM = (255, 255, 255)

    while True:
        # -------------------------------
        # Capture frame & convert to RGB
        # -------------------------------
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)  # Mirror image
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        # -------------------------------
        # Process detected hand landmarks
        # -------------------------------
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                # Get key finger landmarks
                thumb = hand_landmarks.landmark[4]
                index = hand_landmarks.landmark[8]
                middle = hand_landmarks.landmark[12]

                thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
                index_x, index_y = int(index.x * w), int(index.y * h)
                middle_x, middle_y = int(middle.x * w), int(middle.y * h)

                # -------------------------------
                # Draw circles & lines for visualization
                # -------------------------------
                cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 150, 150), -1)
                cv2.circle(frame, (index_x, index_y), 10, (255, 150, 150), -1)
                cv2.circle(frame, (middle_x, middle_y), 10, (255, 150, 150), -1)

                cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), colorTI, 3)
                cv2.line(frame, (thumb_x, thumb_y), (middle_x, middle_y), colorTM, 3)

                # Midpoints of lines (used for cursor control)
                midPointXTI = int((thumb_x + index_x)/2)
                midPointYTI = int((thumb_y + index_y)/2)
                midPointXTM = int((thumb_x + middle_x)/2)
                midPointYTM = int((thumb_y + middle_y)/2)

                cv2.circle(frame, (midPointXTI, midPointYTI), 10, colorTI, -1)
                cv2.circle(frame, (midPointXTM, midPointYTM), 10, colorTM, -1)

                # -------------------------------
                # Measure distance between fingers
                # -------------------------------
                length_lineTI = math.sqrt((thumb_x - index_x)**2 + (thumb_y - index_y)**2)
                length_lineTM = math.sqrt((thumb_x - middle_x)**2 + (thumb_y - middle_y)**2)

                # -------------------------------
                # Left click control
                # -------------------------------
                if length_lineTI < 19:
                    colorTI = (0, 0, 255)
                    if not holding_left:
                        pyautogui.mouseDown(button='left')
                        holding_left = True
                else:
                    colorTI = (255, 255, 255)
                    if holding_left:
                        holding_left = False
                        pyautogui.mouseUp(button='left')

                # -------------------------------
                # Right click control
                # -------------------------------
                if length_lineTM < 23:
                    colorTM = (0, 255, 0)
                    if not holding_right:
                        pyautogui.mouseDown(button='right')
                        holding_right = True
                else:
                    colorTM = (255, 255, 255)
                    if holding_right:
                        pyautogui.mouseUp(button='right')
                        holding_right = False

                # -------------------------------
                # Move mouse based on thumb-index midpoint
                # -------------------------------
                screen_x = int(remap(midPointXTI, old_min=60, old_max=260, new_min=0, new_max=screen_w))
                screen_y = int(remap(midPointYTI, old_min=60, old_max=180, new_min=0, new_max=screen_h))
                prev_x = int(prev_x + (screen_x - prev_x) * smooth_factor)
                prev_y = int(prev_y + (screen_y - prev_y) * smooth_factor)
                pyautogui.moveTo(prev_x, prev_y)

        # -------------------------------
        # Display camera frame
        # -------------------------------
        cv2.imshow("cam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# -------------------------------
# Cleanup
# -------------------------------
cap.release()
cv2.destroyAllWindows()
