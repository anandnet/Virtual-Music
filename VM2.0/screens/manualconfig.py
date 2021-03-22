import cv2
import numpy as np
from widgets.kivycamera import KivyCamera
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty,NumericProperty
from kivy.lang import Builder
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

<ManualConfigScreen>:
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
                AnchorLayout:
                    MDRaisedButton:
                        text: "FIX HSV"
                        md_bg_color: 1, 0, 1, 1
                        on_release:
                            root.save_hsv()


            
""")


class Camera(KivyCamera):
    def on_update(self, frame):
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #print(self.parent.parent.parent.parent.parent.ids.hsv.children)
        children=self.parent.parent.parent.parent.parent.ids
        lower_blue = np.array([int(children.min_h.ids.sld.value),int(children.min_s.ids.sld.value),int(children.min_v.ids.sld.value)])
        upper_blue = np.array([int(children.max_h.ids.sld.value),int(children.max_s.ids.sld.value),int(children.max_v.ids.sld.value)])
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)
        return res


class ManualConfigScreen(Screen):
    cap=None
    def on_enter(self, *args):
        Clock.schedule_once(self.add_camera,1/1000)

    def add_camera(self,*args):
        self.cap=cv2.VideoCapture(0)
        cam=Camera(self.cap)
        self.ids.feed.add_widget(cam)

    def on_pre_leave(self, *args):
        if(self.cap):
            self.cap.release()

    def save_hsv(self):
        ob=self.ids
        hsv_values=np.array([[ob.min_h.ids.sld.value,ob.min_s.ids.sld.value,ob.min_v.ids.sld.value],[ob.max_h.ids.sld.value,ob.max_s.ids.sld.value,ob.max_v.ids.sld.value]])
        np.savetxt('temp/hsv.txt',hsv_values)
