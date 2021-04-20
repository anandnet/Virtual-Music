from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import (
    ColorProperty,
    NumericProperty,
)

Builder.load_string("""
<Loader>:
    size_hint_y:None
    height:"5dp"
    canvas:
        Color:
            rgba:root.bg_color
        RoundedRectangle:
            pos:self.pos
            size:self.size
            radius:[2.5]*4
    BoxLayout:
        size_hint_y:1
        size_hint_x:root.value/100
        canvas:
            Color:
                rgba:root.fill_color
            RoundedRectangle:
                pos:self.pos
                size:self.size
                radius:[2.5]*4
    BoxLayout:
        size_hint_y:1
        size_hint_x:1-root.value/100
        canvas:
            Color:
                rgba:[0,0,0,0]
            RoundedRectangle:
                pos:self.pos
                size:self.size
                radius:[2.5]*4
""")
class Loader(BoxLayout):
    value=NumericProperty(0)
    bg_color=ColorProperty([.7,.7,.7,1])
    fill_color=ColorProperty([.9,.9,.9,1])

    def __init__(self,bg_color=[.7,.7,.7,1],fill_color=[.9,.9,.9,1],value=0 ,**kwargs):
        self.bg_color=bg_color
        self.fill_color=fill_color
        self.value=value
        self.anim=Clock.schedule_interval(self.update_anim, 4.3/100)
        super().__init__(**kwargs)

    def update_anim(self,*args):
        if(self.value>100):
            self.anim.cancel()
        else:
            self.value+=1


