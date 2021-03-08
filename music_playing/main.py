import numpy as np 
import cv2 
from collections import deque

#from kivy.core.audio import SoundLoader
from pygame import mixer
import os

from tensorflow.python import framework
PATH = os.path.dirname(os.path.abspath(__file__))
piano2 = os.path.join(PATH, "assets", "piano2")


class Music():

    already_in_blue = False
    already_in_red = False
    already_in_yellow = False

    def __init__(self):
        mixer.init()
        self.kick = mixer.Sound(os.path.join(PATH, "untitled_a_kick_01.wav"))
        self.hhat = mixer.Sound(os.path.join(PATH, "beachparty_a_hihat_01.wav"))
        self.snare = mixer.Sound(os.path.join(PATH, "beachparty_a_snare_01.wav"))

    def play(self,frame):
        

        #sound = SoundLoader.load('untitled_a_kick_01.wav')
        #kick = mixer.music.load("untitled_a_kick_01.wav")
        
        #sound.loop=  True

        color = Colors()

        # Creating the trackbars needed for  
        # adjusting the marker colour These  
        # trackbars will be used for setting  
        # the upper and lower ranges of the 
        # HSV required for particular colour

        blue=np.loadtxt("data/blue.txt",dtype=np.int)
        green=np.loadtxt("data/green.txt",dtype=np.int)
        red= np.loadtxt("data/red.txt",dtype=np.int)

        blueLower = blue[0]#np.array([55, 146, 36]) #55, 146, 36   #100,60,60 -old
        blueUpper = blue[1]#np.array([168, 255, 255]) #168, 255, 255 #120,255,255

        redLower_1 = red[0]#np.array([134, 174, 61]) # 0, 189, 65  #0,80,80    #129, 188, 92
        redUpper_1 = red[1]#np.array([198,255,255]) # 255, 255, 255   #10,255,255

        redLower_2 = np.array([170,80,80])
        redUpper_2 = np.array([180,255,255])

        yellowLower = green[0]#np.array([16, 89, 49]) #16, 89, 49 #23, 41, 133
        yellowUpper = green[1]#np.array([70, 255, 233]) # 70, 255, 233   #40, 150, 255

        purple_lower = [114, 104, 101]
        purple_upper = [145, 148, 243]

        # ([17, 15, 100], [50, 56, 200]), red
        # 	([86, 31, 4], [220, 88, 50]), blue
        # 	([25, 146, 190], [62, 174, 250]), yellow
        
        # Giving different arrays to handle colour 
        # points of different colour These arrays  
        # will hold the points of a particular colour 
        # in the array which will further be used 
        # to draw on canvas 
        bpoints = [deque(maxlen = 1024)] 
        gpoints = [deque(maxlen = 1024)] 
        rpoints = [deque(maxlen = 1024)] 
        ypoints = [deque(maxlen = 1024)] 
        
        # These indexes will be used to mark position 
        # of pointers in colour array 
        blue_index = 0
        green_index = 0
        red_index = 0
        yellow_index = 0
        
        # The kernel to be used for dilation purpose  
        kernel = np.ones((5, 5), np.uint8) 
        
        # The colours which will be used as ink for 
        # the drawing purpose 
        colors = [(255, 0, 0), (0, 255, 0),  
                (0, 0, 255), (0, 255, 255)] 
        colorIndex = 0
        
        #cv2.namedWindow('Paint', cv2.WINDOW_FREERATIO)
        #cv2.resizeWindow('Paint', 700, 700)
        
        # Flipping the frame to see same side of yours 
        frame = cv2.flip(frame, 1)
        #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        h,w,c= frame.shape
        cv2.rectangle(frame, (10, h//2 + 50), (w-10, h//2 - 100), (0,255,0), 2)
        cropped_frame = hsv[h//2 - 100:h//2 + 50,10:w-10]
        #cropped_frameq = cv2.GaussianBlur(cropped_frame, (11, 11), 0)
        #cv2.imshow("cropped", cropped_frame)
        # Identifying the pointer by making its  
        # mask 
        Mask_blue = cv2.inRange(cropped_frame, blueLower, blueUpper) 
        Mask_blue = cv2.erode(Mask_blue, kernel, iterations = 1) 
        Mask_blue = cv2.morphologyEx(Mask_blue, cv2.MORPH_OPEN, kernel) 
        Mask_blue = cv2.dilate(Mask_blue, kernel, iterations = 1)

        Mask_red = cv2.inRange(cropped_frame, redLower_1, redUpper_1)
        #Mask_red_2 = cv2.inRange(cropped_frame, redLower_2, redUpper_2)
        #Mask_red = Mask_red_1

        Mask_red = cv2.erode(Mask_red, kernel, iterations = 1) 
        Mask_red = cv2.morphologyEx(Mask_red, cv2.MORPH_OPEN, kernel) 
        Mask_red = cv2.dilate(Mask_red, kernel, iterations = 1)

        Mask_yellow = cv2.inRange(cropped_frame, yellowLower, yellowUpper) 
        Mask_yellow = cv2.erode(Mask_yellow, kernel, iterations = 1) 
        Mask_yellow = cv2.morphologyEx(Mask_yellow, cv2.MORPH_OPEN, kernel) 
        Mask_yellow = cv2.dilate(Mask_yellow, kernel, iterations = 1) 
    
        # Find contours for the pointer after  
        # idetifying it 
        cnts_blue, _ = cv2.findContours(Mask_blue.copy(), cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)
        
        cnts_red, _ = cv2.findContours(Mask_red.copy(), cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)
        
        cnts_yellow, _ = cv2.findContours(Mask_yellow.copy(), cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)
        radius_=25
        if len(cnts_blue) > 0:
            
            # sorting the contours to find biggest  
            cnt = max(cnts_blue, key = cv2.contourArea)

            # Calculating the center of the detected contour 
            # M = cv2.moments(cnt) 
            # center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            # Get the radius of the enclosing circle  
            # around the found contour 
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            #print( center, (x, y))
            print(int(y)+(h//2 - 100) + radius , (h//2 + 50+5))

            if int(y)+(h//2 - 100) + radius_ > (h//2 + 40+5):
                print("already in blue")
                if not self.already_in_blue:
                    print("green")
                #if not mixer.music.get_busy():
                    self.kick.play()
                
                self.already_in_blue = True
                #if sound:
                    #print("Sound AVailable")
                #    print(sound.state)
                #    sound.play()
                    #print("Not availabe")
                clr = color.cyan
                #cv2.circle(frame, (int(x)+10, int(y)+(h//2 - 100)), int(radius), color.cyan, 2)
            else:
            
                self.already_in_blue = False
                #sound.stop()
                #sound.unload()
                clr = color.blue
            
            cv2.circle(frame, (int(x)+10, int(y)+(h//2 - 100)), radius_, clr, 2) 

        if len(cnts_red) > 0:
            
            # sorting the contours to find biggest  
            cnt = max(cnts_red, key = cv2.contourArea)

            # Calculating the center of the detected contour 
            # M = cv2.moments(cnt) 
            # center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            # Get the radius of the enclosing circle  
            # around the found contour 
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            
            #print( center, (x, y))
            if int(y)+(h//2 - 100) + radius_ > (h//2 + 40+5):
                
                if not self.already_in_red:
                #if not mixer.music.get_busy():
                    self.hhat.play()
                
                already_in_red = True
                #if sound:
                    #print("Sound AVailable")
                #    print(sound.state)
                #    sound.play()
                    #print("Not availabe")
                clr = color.cyan
                #cv2.circle(frame, (int(x)+10, int(y)+(h//2 - 100)), int(radius), color.cyan, 2)
            else:
            
                self.already_in_red = False
                #sound.stop()
                #sound.unload()
                clr = color.red
            
            cv2.circle(frame, (int(x)+10, int(y)+(h//2 - 100)), radius_, clr, 2) 
        
        if len(cnts_yellow) > 0:
            
            # sorting the contours to find biggest  
            cnt = max(cnts_yellow, key = cv2.contourArea)

            # Calculating the center of the detected contour 
            # M = cv2.moments(cnt) 
            # center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            # Get the radius of the enclosing circle  
            # around the found contour 
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            print("out out yellow")
            #print( center, (x, y))
            print(int(y)+(h//2 - 100) + radius , (h//2 + 50+5))
            if int(y)+(h//2 - 100) + radius_ > (h//2 + 40+5):
                #print("already in yellow")
                if not self.already_in_yellow:
                    #print("green")
                #if not mixer.music.get_busy():
                    self.snare.play()
                
                self.already_in_yellow = True
                #if sound:
                    #print("Sound AVailable")
                #    print(sound.state)
                #    sound.play()
                    #print("Not availabe")
                clr = color.cyan
                #cv2.circle(frame, (int(x)+10, int(y)+(h//2 - 100)), int(radius), color.cyan, 2)
            else:
            
                self.already_in_yellow = False
                #sound.stop()
                #sound.unload()
                clr = color.yellow
            
            cv2.circle(frame, (int(x)+10, int(y)+(h//2 - 100)), radius_, color.green, 2) 
            
            

            #print(center)
            # Now checking if the user wants to click on  
            # any button above the screen

            #print(center)
                    
        # Append the next deques when nothing is  
        # detected to avois messing up
    
        # Draw lines of all the colors on the 
        # canvas and frame  
        # points = [bpoints, gpoints, rpoints, ypoints] 
        # for i in range(len(points)): 
            
        #     for j in range(len(points[i])): 
                
        #         for k in range(1, len(points[i][j])): 
                    
        #             if points[i][j][k - 1] is None or points[i][j][k] is None: 
        #                 continue
                        
        #             cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2) 
        #             cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2) 
        return frame

class Colors():
    red = (0, 0, 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)
    yellow = (0, 255, 255)
    cyan = (255, 228, 0) 

if __name__ == '__main__':
    cap=cv2.VideoCapture(0)
    music=Music()
    while True:
        ret,frame=cap.read()
        img=music.play(frame)
        cv2.imshow("Image",img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release() 
            cv2.destroyAllWindows()
            break
