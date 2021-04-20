from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang.builder import Builder
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ColorProperty,
    NumericProperty
)
import utils.theme as theme

Builder.load_string("""
<DropItem>:
    dummy_clr:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
    canvas:
        Color:
            rgba:(1,1,1,0) if root.transparent else (0.05,0.05,.05,1) if app.theme_cls.theme_style=="Dark" else (0.95,.95,.95,1)
        Rectangle:
            pos:self.pos
            size:self.size

    size_hint_y:None
    height:"40dp"
    padding:20,0,20,0
    MDIcon:
        size_hint_x:None
        width:"40dp"
        icon:root.icon
        color:root.dummy_clr if root.icon_color[3]==0 else root.icon_color
    MDLabel:
        text:root.text
        color:root.dummy_clr if root.icon_color[3]==0 else root.icon_color
        font_size:root.font_size
        #color:1,1,1,1
""")


class DropItem(ButtonBehavior, BoxLayout):
    transparent = BooleanProperty()
    icon = StringProperty()
    text = StringProperty()
    icon_color = ColorProperty()
    font_size=NumericProperty()

    def __init__(self,icon_color=[0,0,0,0], icon="android", text="", transparent=False,font_size=18 , ** kwargs):
        self.icon = icon
        self.text = text
        self.icon_color = icon_color
        self.transparent = transparent
        self.font_size=font_size
        super().__init__(**kwargs)

    def on_release(self):
        pass
