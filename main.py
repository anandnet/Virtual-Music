from hand_tracking.utils import detector_utils as detector_utils
import cv2
import tensorflow as tf
import datetime

detection_graph, sess = detector_utils.load_inference_graph()

if __name__ == '__main__':

    fps=1 #for showing fps
    width=320
    height=2400
    score_thresh=0.2 #Score threshold for displaying bounding boxes
    cap = cv2.VideoCapture(0)
    start_time = datetime.datetime.now()
    num_frames = 0
    im_width, im_height = (320,240)
    # max number of hands we want to detect/track
    num_hands_detect = 1

    cv2.namedWindow('Single-Threaded Detection', cv2.WINDOW_NORMAL)

    while True:
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        ret, image_np = cap.read()
        image_np=cv2.resize(image_np,(im_width,im_height))
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")

        boxes, scores = detector_utils.detect_objects(image_np,
                                                      detection_graph, sess)

        # draw bounding boxes on frame
        roi=detector_utils.roi_image(num_hands_detect, score_thresh,
                                         scores, boxes, im_width, im_height,
                                         image_np)

        # Calculate Frames per second (FPS)
        num_frames += 1
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        fps = num_frames / elapsed_time

        
        if (fps > 0):
            detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                                image_np)

        cv2.imshow('Single-Threaded Detection',
                    cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
        
        if(roi is not None):
            cv2.imshow("ROI",roi)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
