from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
Builder.load_string("""
<HelpScreen>:
    BoxLayout:
        canvas:
            Color:
                rgba:theme.get_color(app.theme_cls.theme_style,"BackgroundColor")
            Rectangle:
                pos:self.pos
                size:self.size
""")
class HelpScreen(Screen):
    pass