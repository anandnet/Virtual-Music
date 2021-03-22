from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
Builder.load_string("""
<HelpScreen>:
    BoxLayout:
        canvas:
            Color:
                rgba:1,0.15,1,1
            Rectangle:
                pos:self.pos
                size:self.size
""")
class HelpScreen(Screen):
    pass