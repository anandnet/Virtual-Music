from mediapipe.python import solutions
import cv2
mp_drawing = solutions.drawing_utils
mp_hands = solutions.hands
circle_spec = mp_drawing.DrawingSpec(color=(0, 0, 255), circle_radius=2)
connection_spec = ''
# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.7)


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
    right_hand_status, left_hand_status = None, None
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            if results.multi_handedness[i].classification[0].label == "Right":
                right_hand_status = get_finger_status(
hand_landmarks.landmark,1)

            if results.multi_handedness[i].classification[0].label == "Left":
                left_hand_status = get_finger_status(hand_landmarks.landmark,0)

    
    return left_hand_status,right_hand_status


def get_hands(image, landmark):
    height, width = image.shape[0], image.shape[1]
    x_list = []
    y_list = []
    for i, each in enumerate(landmark):
        x_list.append(each.x)
        y_list.append(each.y)
    x_min, x_max, y_min, y_max = int(min(x_list)*width)-20, int(
        max(x_list)*width)+20, int(min(y_list)*height)-20, int(max(y_list)*height)+20
    #print(x_min, x_max, y_min, y_max)
    if x_min < 0:
        x_min = 0
    if x_max > width:
        x_max = width
    if y_min < 0:
        y_min = 0
    if y_max > height:
        y_max = height
    crop = image[y_min:y_max, x_min:x_max]
    return crop


def get_finger_status(landmark,hnd_index):
    if(hnd_index==0):
        thumb = is_fingure_close(landmark[4].x, landmark[3].x, landmark[2].x)
    else:
        thumb = is_fingure_close(landmark[2].x, landmark[3].x, landmark[4].x)

    index = is_fingure_close(landmark[6].y, landmark[7].y, landmark[8].y)
    middle = is_fingure_close(landmark[10].y, landmark[11].y, landmark[12].y)
    ring = is_fingure_close(landmark[14].y, landmark[15].y, landmark[16].y)
    little = is_fingure_close(landmark[18].y, landmark[19].y, landmark[20].y)
    palm_up = not thumb and not index and not middle and not ring and not little
    #palm_dowm = thumb and index and middle and ring and little
    return [palm_up, thumb, index, middle, ring, little]


def is_fingure_close(fixkeypoint, point1, point2):
    return point1 > fixkeypoint and point2 > fixkeypoint
