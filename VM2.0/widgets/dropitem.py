from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang.builder import Builder
from kivy.properties import (
    StringProperty,
    BooleanProperty,
)

Builder.load_string("""
<DropItem>:
    canvas:
        Color:
            rgba:(1,1,1,0) if root.transparent else (0.05,0.05,.05,1) if app.theme_cls.theme_style=="Dark" else (0.9,.9,.9,1)
        Rectangle:
            pos:self.pos
            size:self.size

    size_hint_y:None
    height:40
    padding:20,0,20,0
    MDIcon:
        icon:root.icon
        color:1,1,1,1
    MDLabel:
        text:root.text
        color:1,1,1,1
""")


class DropItem(ButtonBehavior,BoxLayout):
    transparent=BooleanProperty()
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, icon="android",text="",transparent=False,**kwargs):
        self.icon=icon
        self.text=text
        self.transparent=transparent
        super().__init__(**kwargs)

    def on_release(self):
        print("hello")
