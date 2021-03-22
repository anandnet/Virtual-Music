__all__ = ("Selector")
from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard
from kivy.uix.behaviors import ToggleButtonBehavior
from kivymd.uix.behaviors.elevation import CommonElevationBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    ColorProperty,
    StringProperty,
    NumericProperty,
)
from utils.selected_instrument import inst_indx

Builder.load_string("""
<InstrumentSelector>:
    radius:[10,10,10,10]
    size_hint:None,None
    height:150
    width:130
    padding:0,15,0,0
    orientation:"vertical"
    canvas:
        Color:
            rgba:[.5,.5,.5,.5] if self.active else self.color
        RoundedRectangle:
            pos:self.pos
            size:self.size
            #radius:root.radius
    Image:
        source: root.source
        size: self.texture_size
    MDLabel:
        halign:"center"
        text: root.text
        theme_text_color:"Secondary"
""")


class InstrumentSelector(MDCard, CommonElevationBehavior, ToggleButtonBehavior, HoverBehavior):
    active = BooleanProperty(False)
    source = StringProperty()
    text = StringProperty()
    color = ColorProperty([.1, .1, .1, .3])

    def on_state(self,  widget, value):
        l = ["Piano", "Guitar", "Violin", "Xylophone", "Drums"]
        if value == "down":
            self.active = True
            _list = ToggleButtonBehavior.get_widgets('m')
            for each in _list:
                if each is not widget:
                    each.active = False
                    each.color = [.1, .1, .1, .3]
            del _list
            ind = l.index(widget.text)
            import utils.selected_instrument as ut
            ut.inst_indx = ind
            st = "inst_indx = {}".format(ind)

            with open('utils/selected_instrument.py', 'w') as file:
                file.write(st)

    def on_enter(self):
        if(not self.active):
            self.color = [.3, .3, .3, .5]
            pass

    def on_leave(self):
        if(not self.active):
            self.color = [.1, .1, .1, .3]
            pass
