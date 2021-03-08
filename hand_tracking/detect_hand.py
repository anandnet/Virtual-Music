import mediapipe as mp
import cv2
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
circle_spec = mp_drawing.DrawingSpec(color=(0, 0, 255), circle_radius=2)
connection_spec = ''
# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)


def detect_hand(frame):

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    right_hand, left_hand = None, None
    blank_image = np.zeros((image.shape[0],image.shape[1],3), np.uint8)
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            if results.multi_handedness[i].classification[0].label == "Right":
                blank_image = get_hands(image,blank_image, hand_landmarks.landmark)
            if results.multi_handedness[i].classification[0].label == "Left":
                blank_image = get_hands(image,blank_image, hand_landmarks.landmark)
    
    return blank_image


def get_hands(image,blank, landmark):
    height, width = image.shape[0], image.shape[1]
    x_list = []
    y_list = []
    for each in landmark:
        x_list.append(each.x)
        y_list.append(each.y)
    x_min, x_max, y_min, y_max = int(min(x_list)*width)-20, int(
        max(x_list)*width)+20, int(min(y_list)*height)-20, int(max(y_list)*height)+20
    # print(x_min, x_max, y_min, y_max)
    if x_min < 0:
        x_min = 0
    if x_max > width:
        x_max = width
    if y_min-30 < 0:
        y_min = 0
    else:
        y_min=y_min-30
    if y_max > height:
        y_max = height
    blank[y_min:y_max, x_min:x_max] = image[y_min:y_max, x_min:x_max]
    return blank
