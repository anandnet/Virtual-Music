from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
Builder.load_string("""
<SettingScreen>:
    BoxLayout:
        canvas:
            Color:
                rgba:1,0.15,0.15,1
            Rectangle:
                pos:self.pos
                size:self.size
""")

class SettingScreen(Screen):
    pass