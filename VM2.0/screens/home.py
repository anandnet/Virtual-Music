from itertools import count
from kivy.clock import Clock
from widgets.kivycamera import KivyCamera
import cv2
import numpy as np
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from utils.predict import Predict
from utils.selected_instrument import inst_indx
from handtracking.detect_hand import detect_hand

Builder.load_string("""
<HomeScreen>:
    #id:home
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
                padding:10
                size_hint_y:.55 if root.height<700 else .5
                size_hint_x:1 if root.width<1000  else .8
                AnchorLayout:
                    id:feed
                    anchor_x:"left"
                    padding:10     

            #Something
            AnchorLayout:
                size_hint_y:.4
                MDLabel:
                    halign:"center"
                    text:"Loading..."
                    id:label
                    theme_text_color:"Primary"
                
                
            
        # blank for right now
        BoxLayout:
            padding:0,0,10,0
            orientation:"vertical"
            size_hint_x:.5
            GridLayout:
                id:instruments
                padding:15,25,15,15
                spacing:15
                cols:3 if root.width>=1000 else 2
                InstrumentSelector:
                    source: 'assets/icons/piano.png'
                    text:"Piano"
                    group:"m"
                InstrumentSelector:
                    source: 'assets/icons/guitar.png'
                    text:"Guitar"
                    group:"m"
                InstrumentSelector:
                    source: 'assets/icons/violin.png'
                    text:"Violin"
                    group:"m"
                InstrumentSelector:
                    source: 'assets/icons/xylophone.png'
                    text:"Xylophone"
                    group:"m"
                InstrumentSelector:
                    source: 'assets/icons/drums.png'
                    text:"Drums"
                    group:"m"

            BoxLayout:
                MDRaisedButton:
                    text:"Start"
                    on_release:
                        root.ids.feed.children[0].flag=1
                        root.ids.feed.children[0]._count=499
                MDRaisedButton:
                    text:"Change Class"
                    on_release:
                        root.ids.feed.children[0]._class+=1
            
""")


class Camera(KivyCamera):
    flag = 0
    _count = 0
    _class = 0

    def __init__(self, cap, **kwargs):
        super().__init__(cap, **kwargs)
        self.prediction = Predict()

    def on_update(self, frame):
        [left, l_index], [right, r_index] = detect_hand(frame, args=2)
        left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
        right = cv2.cvtColor(cv2.flip(right, 1), cv2.COLOR_BGR2GRAY)
        str_ = self.prediction.predict(
            0, cv2.resize(left, (100, 100)), l_index)
        str__ = self.prediction.predict(
            1, cv2.resize(right, (100, 100)), r_index)
        self.parent.parent.parent.parent.parent.ids.label.text = "Left: "+str_+"  Right: "+str__

        # Dataset Creater

        import time
        if self.flag == 1:
            self._count += 1
            if(self._count < 1001):
                time.sleep(0.05)
                self.parent.parent.parent.parent.parent.ids.label.text = "class: " + \
                    str(self._class)+"==>"+str(self._count)
                import os.path
                if(self._count % 10 == 0):
                    filename2 = os.path.join(
                        "dummy_test_ds/{}/10-03_{}_".format(self._class, self._class)+str(self._count)+".jpg")
                    cv2.imwrite(filename2, left)
                else:
                    filename = os.path.join(
                        "dummy_ds/{}/10-03_{}_".format(self._class, self._class)+str(self._count)+".jpg")
                    cv2.imwrite(filename, left)

                print(self._count)
            else:
                self.flag = 0

        return frame


class HomeScreen(Screen):

    cap = None

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.add_camera, 1/1000)
        Clock.schedule_once(self.set_instrument, 1/1000)

    def set_instrument(self, *args):
        for each in self.ids.instruments.children:
            if(each.text == ["Piano", "Guitar", "Violin", "Xylophone", "Drums"][inst_indx]):
                each.active = True

    def add_camera(self, *args):
        source = 0  # "https://192.168.43.1:8080/video"
        self.cap = cv2.VideoCapture(source)
        cam = Camera(self.cap)
        self.ids.feed.add_widget(cam)

    def on_pre_leave(self, *args):
        # print("hello")
        if(self.cap):
            self.cap.release()
        # self.ids.feed.remove_widget(self.ids.feed.children[0])
        pass
