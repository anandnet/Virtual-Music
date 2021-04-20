import cv2
import random
from functools import partial
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.uix import boxlayout
from widgets.kivycamera import KivyCamera
from widgets.selector import InstrumentSelector
from utils.constant import clr
from utils.play_music import Music
from utils.constant import instruments_items
from handtracking.detect_hand import detect_hand
from kivy.properties import (
    ColorProperty,
    StringProperty,
    NumericProperty,
)

Builder.load_string("""
<AnimIcon>:
    size_hint:None,None
    height:self.minimum_height
    width:self.minimum_width
    MDIcon:
        color:root.color
        icon:root.icon
        halign:"center"
        font_size:root.font_size
<HomeScreen>:
    #id:home
    BoxLayout:
        canvas:
            Color:
                rgba:theme.get_color(app.theme_cls.theme_style,"BackgroundColor")
            Rectangle:
                pos:self.pos
                size:self.size
        #camera + something
        BoxLayout:
            orientation:"vertical"
            size_hint_x:.5
            #Camera
            BoxLayout:
                padding:"10dp"
                size_hint_y:.55 if root.height<700 else .5
                size_hint_x:1 if root.width<1000  else .8
                AnchorLayout:
                    id:feed
                    anchor_x:"left"
                    padding:10     

            #Something
            BoxLayout:
                size_hint_y:.4
                size_hint_x:1 if root.width<1000  else .8
                FloatLayout:
                    id:music
                    
                
                
                
            
        # blank for right now
        BoxLayout:
            padding:0,0,10,0
            orientation:"vertical"
            size_hint_x:.5
            ScrollView:
                do_scroll_y:True
                GridLayout:
                    size_hint_y:None
                    height:self.minimum_height
                    id:instruments
                    padding:15,25,15,15
                    spacing:"15dp"
                    cols:3 if root.width>=1000 else 2
                    InstrumentSelector:
                        source: 'assets/icons/piano_white.png' if self.active else 'assets/icons/piano.png'
                        text:"Piano"
                        group:"m"
                        default_instrument:True
                    InstrumentSelector:
                        source: 'assets/icons/guitar_white.png' if self.active else 'assets/icons/guitar1.png' 
                        text:"Guitar"
                        group:"m"
                        default_instrument:True
                    InstrumentSelector:
                        source: 'assets/icons/violin_white.png' if self.active else 'assets/icons/violin.png'
                        text:"Violin"
                        group:"m"
                        default_instrument:True
                    InstrumentSelector:
                        source: 'assets/icons/xylophone_white.png' if self.active else 'assets/icons/xylophone.png'
                        text:"Xylophone"
                        group:"m"
                        default_instrument:True
                    InstrumentSelector:
                        source: 'assets/icons/drums_white.png' if self.active else 'assets/icons/drums.png'
                        text:"Drums"
                        group:"m"
                        default_instrument:True
            
""")


class Camera(KivyCamera):

    def __init__(self, cap, **kwargs):
        super().__init__(cap, **kwargs)
        self.music = Music()

    def on_update(self, frame):
        left_status, right_status = detect_hand(frame)
        #print(left_status, right_status)
        Clock.schedule_once(partial(self.play, left_status, 0))
        Clock.schedule_once(partial(self.play, right_status, 1))

        return frame

    def play(self, status, hand_indx, interval):
        if(status):
            true_index = [i for i, each in enumerate(status) if each == True]
            if(len(true_index) == 1):
                self.music.play(hand_indx, true_index[0])
                if(true_index[0] != 0):
                    self.add_anim()

    def add_anim(self):
        icon = AnimIcon(
            color=random.choice(clr),
            icon=random.choice(
                ["music-clef-treble", "music", "music-note"]),
            pos_hint={"y": 0, "x": .45}
        )
        self.parent.parent.parent.parent.parent.ids.music.add_widget(icon)


class HomeScreen(Screen):

    cap = None

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.add_camera, 1/1000)
    def on_enter(self):
        Clock.schedule_once(self.add_manual_instrument, 1/1000)

    def add_manual_instrument(self, *args):
        #print(self.ids.instruments.children)
        #print("\n\nRemoving list")
        for each in self.ids.instruments.children:
            #print(each.text)
            if not each.default_instrument:
                #print(each.text)
                self.ids.instruments.remove_widget(each)
        #print("After Removing",[each.text for each in self.ids.instruments.children])
        
        #print("\n\nAdding list")
        import  utils.selected_instrument as ut
        for each in ut.manual_instr:
            #print(each)
            inst = InstrumentSelector(text=each.capitalize(), source="")
            inst.group = 'm'
            self.ids.instruments.add_widget(inst)

        #print("after Adding",[each.text for each in self.ids.instruments.children])
        self.set_instrument(instruments_items+ut.manual_instr,ut)

    def set_instrument(self, all_instruments,ut):
        if(ut.selected_instr not in all_instruments):
            ut.selected_instr="piano"
            st = "selected_instr = '{}'\ncamera_indx = {}\nmanual_instr = {}".format(
                ut.selected_instr, ut.camera_indx, ut.manual_instr)

            with open('utils/selected_instrument.py', 'w') as file:
                file.write(st)
        
        for each in self.ids.instruments.children:
            if(each.text == ut.selected_instr.capitalize()):
                each.active = True
            else:
                each.active = False

    def add_camera(self, *args):
        try:
            import utils.selected_instrument as ut
            from pygrabber.dshow_graph import FilterGraph
            device = FilterGraph().get_input_devices()[ut.camera_indx]
        except:
            ut.camera_indx = 0
            st = "selected_instr = '{}'\ncamera_indx = {}\nmanual_instr = {}".format(
                ut.selected_instr, 0, ut.manual_instr)

            with open('utils/selected_instrument.py', 'w') as file:
                file.write(st)

        source = ut.camera_indx  # "https://192.168.43.1:8080/video"
        self.cap = cv2.VideoCapture(source)
        cam = Camera(self.cap)
        self.ids.feed.add_widget(cam)

    def on_pre_leave(self, *args):
        # print("hello")
        if(self.cap):
            self.cap.release()
        # self.ids.feed.remove_widget(self.ids.feed.children[0])
        pass


class AnimIcon(BoxLayout):
    color = ColorProperty()
    font_size = NumericProperty()
    icon = StringProperty()

    def __init__(self, icon, color=[0, 0, 1, 0], font_size="20sp", **kwargs):
        self.color = color
        self.font_size = font_size
        self.icon = icon
        super(AnimIcon, self).__init__(**kwargs)
        Clock.schedule_once(self.start_anim, 1/1000)

    def start_anim(self, *args):

        anim = Animation(color=random.choice(clr),
                         font_size=70,
                         pos_hint={"x": random.randrange(
                             25, 75, 5)/100, "y": .95},
                         duration=3
                         )
        anim.start(self)
        Clock.schedule_once(partial(self.remove_wid, self), 3)

    def remove_wid(self, inst, args):
        self.parent.remove_widget(inst)
