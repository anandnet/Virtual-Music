import mediapipe as mp
import cv2
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
circle_spec=mp_drawing.DrawingSpec(color=(0, 0, 255),circle_radius=2)
connection_spec=''
# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

def detect_hand(frame,args=1):
    """
    frame = input frame
    * args=0, for cropped part of left hand
    * args=1 (default), for cropped part of right hand
    * args=2, for both 0 and 1 returned a touple (left,right)
    * trainig_images, by default False, if it is true it will return image of hand skeleten of shape (100,100,3)
    (After return one flip required for mirror image)

    """
    
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
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            if results.multi_handedness[i].classification[0].label == "Right":
                right_hand = [get_hands(image, hand_landmarks.landmark,),get_distance(hand_landmarks.landmark)]
                
            if results.multi_handedness[i].classification[0].label == "Left":
                left_hand = [get_hands(image, hand_landmarks.landmark),get_distance(hand_landmarks.landmark)]
                

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,landmark_drawing_spec=circle_spec,)

    
    blank_image = np.zeros((100,100,3), np.uint8)
    
    if(args==0 and left_hand is not None):
        return left_hand
    
    if(args==1 and right_hand is not None):
        return right_hand

    if(args==2 and left_hand is not None and right_hand is not None):
        return left_hand,right_hand
    elif(args==2 and left_hand is not None):
        return left_hand,[blank_image,None]
    elif(args==2 and right_hand is not None):
        return [blank_image,None],right_hand
    elif(args==2):
        return [blank_image,None],[blank_image,None]
    
    return blank_image

def get_hands(image, landmark):
    height, width = image.shape[0], image.shape[1]
    x_list = []
    y_list = []
    for i,each in enumerate(landmark):
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


def get_distance(landmarks):
    import math
    list_=[]
    list_.append(math.dist((landmarks[4].x,landmarks[4].y), (landmarks[2].x,landmarks[2].y)))
    list_.append(math.dist((landmarks[8].x,landmarks[8].y), (landmarks[5].x,landmarks[5].y)))
    list_.append(math.dist((landmarks[12].x,landmarks[12].y), (landmarks[9].x,landmarks[9].y)))
    list_.append(math.dist((landmarks[16].x,landmarks[16].y), (landmarks[13].x,landmarks[13].y)))
    list_.append(math.dist((landmarks[20].x,landmarks[20].y), (landmarks[17].x,landmarks[17].y)))
    ind=np.argmin(list_)
    return ind+1