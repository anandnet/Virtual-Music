__all__ = ("Selector")
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import (
    HoverBehavior)
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    StringProperty,
)
from utils.selected_instrument import selected_instr
import utils.theme as theme

Builder.load_string("""
<InstrumentSelector>:
    #radius:[40,40,40,40]
    #elevation:0
    size_hint:None,None
    height:"150dp"
    width:"130dp"
    padding:0,15,0,0
    orientation:"vertical"
    canvas:
        Color:
            rgba:theme.get_color(app.theme_cls.theme_style,"SelectorActiveColor") if self.active else self.color if self.hovered else theme.get_color(app.theme_cls.theme_style, "SelectorNormalColor")   #[1,0,1,.5]
        RoundedRectangle:
            pos:self.pos
            size:self.size
            #radius:root.radius
    Image:
        source:('assets/icons/drums_white.png' if root.active else 'assets/icons/drums.png') if root.source=="" else root.source
        size: self.texture_size
    MDLabel:
        halign:"center"
        text: root.text
        #theme_text_color:"Primary" if root.active else "Secondary"
        color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor") if root.active else theme.get_color(app.theme_cls.theme_style,"SecondaryTextColor")
""")


class InstrumentSelector(ToggleButtonBehavior, HoverBehavior, ThemableBehavior,  BoxLayout):
    active = BooleanProperty(False)
    source = StringProperty()
    text = StringProperty()
    color = ColorProperty([.1, .1, .1, .3])
    default_instrument=BooleanProperty()

    def __init__(self, text="", source="",default_instrument=False, **kwargs):
        self.text = text
        self.source = source
        self.default_instrument=default_instrument
        super(InstrumentSelector, self).__init__(**kwargs)

    def on_state(self,  widget, value):
        #l = ["Piano", "Guitar", "Violin", "Xylophone", "Drums"]
        if value == "down":
            self.active = True
            _list = ToggleButtonBehavior.get_widgets('m')
            for each in _list:
                if each is not widget:
                    each.active = False
                    each.color = theme.get_color(
                        self.theme_cls.theme_style, "SelectorNormalColor")  # [.1, .1, .1, .3]
            del _list
            name = widget.text.lower()
            import utils.selected_instrument as ut
            ut.selected_instr = name
            st = "selected_instr = '{}'\ncamera_indx = {}\nmanual_instr = {}".format(
                name, ut.camera_indx, ut.manual_instr)

            with open('utils/selected_instrument.py', 'w') as file:
                file.write(st)

    def on_enter(self):
        if(not self.active):
            self.color = theme.get_color(
                self.theme_cls.theme_style, "SelectorHoverColor")  # [.3, .3, .3, .5]
            pass

    def on_leave(self):
        if(not self.active):
            self.color = theme.get_color(
                self.theme_cls.theme_style, "SelectorNormalColor")  # [.1, .1, .1, .3]
            pass
