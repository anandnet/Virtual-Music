from music_playing.main import Music
import cv2
import numpy as np
from kivycamera import KivyCamera
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from hand_tracking.detect_hand import detect_hand
Builder.load_string("""

<CustomSlider@BoxLayout>:
    value:0
    text:""
    orientation:"vertical"
    size_hint_y:None
    height:50
    BoxLayout:
        size_hint_y:None
        height:10
        padding:20,0,20,0
        MDLabel:
            theme_text_color:"Secondary"#if app.theme_cls.theme_style=="dark" else (0,0,0,1)
            text:root.text+": "+str(int(root.ids.sld.value))
    BoxLayout:
        size_hint_y:None
        height:40
        MDSlider:
            id:sld
            min:0
            max:255
            value:root.value

<MainScreen>:
    BoxLayout:
        canvas:
            Color:
                rgba:0.1,0.1,0.1,1
            Rectangle:
                pos:self.pos
                size:self.size
        #camera + something
        BoxLayout:
            orientation:"vertical"
            size_hint_x:.5
            canvas:
                Color:
                    rgba:0.1,0.1,0.1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
            #Camera
            BoxLayout:
                size_hint_y:.6
                size_hint_x:1
                AnchorLayout:
                    anchor_x:"left"
                    padding:10
                    id:feed

            #Something
            BoxLayout:
                size_hint_y:.4
                AnchorLayout:
                    MDRaisedButton:
                        text: "Hsv Mode"
                        md_bg_color: 1, 0, 1, 1
                        on_release:
                            root.change_mode(self)
                

                
        # hsv sliders
        BoxLayout:
            #orientation:"vertical"
            size_hint_x:.5
            spacing:10
            

            Widget:
                size_hint:(0.4,1)
            BoxLayout:
                spacing:15
                radius:[10]*4
                size_hint:(0.8,1)
                padding:5,10,50,5
                orientation:"vertical"
                canvas:
                    Color:
                        rgba:0.2,0.2,0.2,1
                    Rectangle:
                        pos:self.pos
                        size:self.size
                BoxLayout:
                    size_hint_y:None
                    height:30
                    padding:10
                    MDLabel:
                        text:"Min HSV"
                        theme_text_color:"Primary"
                        font_size:20
                CustomSlider:
                    id:min_h
                    text:"H"
                    value: 0
                CustomSlider:
                    id:min_s
                    text:"S"
                    value: 0
                CustomSlider:
                    id:min_v
                    text:"V"
                    value: 0
                Widget:
                    height:20

                BoxLayout:
                    size_hint_y:None
                    height:30
                    padding:10
                    MDLabel:
                        text:"Max HSV"
                        theme_text_color:"Primary"
                        font_size:20
                CustomSlider:
                    id:max_h
                    text:"H"
                    value: 255
                CustomSlider:
                    id:max_s
                    text:"S"
                    value: 255
                CustomSlider:
                    id:max_v
                    text:"V"
                    value: 255
                BoxLayout:
                    spacing:5
                    MDRaisedButton:
                        text: "FIX Red"
                        md_bg_color: 1, 0, 1, 1
                        on_release:
                            root.save_hsv("r")

                    MDRaisedButton:
                        text: "FIX Green"
                        md_bg_color: 1, 0, 1, 1
                        on_release:
                            root.save_hsv("g")

                    MDRaisedButton:
                        text: "FIX Blue"
                        md_bg_color: 1, 0, 1, 1
                        on_release:
                            root.save_hsv("b")


            
""")


class Camera(KivyCamera):
    def __init__(self, cap, **kwargs):
        self.music = Music()
        super().__init__(cap, **kwargs)
    hsv_mode = False

    def on_update(self, frame):
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if(self.hsv_mode):
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # print(self.parent.parent.parent.parent.parent.ids.hsv.children)
            children = self.parent.parent.parent.parent.parent.ids
            lower_blue = np.array([int(children.min_h.ids.sld.value), int(
                children.min_s.ids.sld.value), int(children.min_v.ids.sld.value)])
            upper_blue = np.array([int(children.max_h.ids.sld.value), int(
                children.max_s.ids.sld.value), int(children.max_v.ids.sld.value)])
            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame, frame, mask=mask)
            return res

        else:
            img = detect_hand(frame)
            img = self.music.play(img)
            return img


class MainScreen(Screen):
    cap = None

    def on_enter(self, *args):
        Clock.schedule_once(self.add_camera, 1/1000)

    def add_camera(self, *args):
        self.cap = cv2.VideoCapture(0)
        cam = Camera(self.cap)
        self.ids.feed.add_widget(cam)

    def on_pre_leave(self, *args):
        if(self.cap):
            self.cap.release()

    def change_mode(self,ins):
        self.ids.feed.children[0].hsv_mode = not self.ids.feed.children[0].hsv_mode
        ins.text = "Normal Mode" if self.ids.feed.children[0].hsv_mode else "Hsv Mode"

    def save_hsv(self, str_):
        ob = self.ids
        hsv_values = np.array([[ob.min_h.ids.sld.value, ob.min_s.ids.sld.value, ob.min_v.ids.sld.value], [
                              ob.max_h.ids.sld.value, ob.max_s.ids.sld.value, ob.max_v.ids.sld.value]])
        if(str_ == "r"):
            np.savetxt('data/red.txt', hsv_values)
        elif(str_ == "b"):
            np.savetxt('data/blue.txt', hsv_values)
        elif(str_ == "g"):
            np.savetxt('data/green.txt', hsv_values)
