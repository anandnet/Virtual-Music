__all__ = ("NavButton")

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    ColorProperty,
    StringProperty,
    NumericProperty,
)
from kivymd.uix.tooltip import MDTooltipViewClass
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.boxlayout import BoxLayout

from logging import fatal
Builder.load_string("""
<NavButton>:
    tooltip_text:"name_icon"
    size_hint_y:None
    height:root.icon_size+20
    BoxLayout:
        size_hint_x:None
        width:2
        canvas:
            Color:
                rgba:(1,1,1,1) if root.active else (1,1,1,0)
            Rectangle:
                pos:self.pos
                size:self.size
    BoxLayout:
        canvas:
            Color:
                rgba:1,1,1,0
            Rectangle:
                pos:self.pos
                size:self.size
        MDIcon:
            id:icon
            font_size: root.icon_size
            halign:"center"
            icon: root.icon
            theme_text_color: "Custom"
            text_color: root.hover_icon_color if root.active else root.normal_icon_color


""")


class NavButton(ToggleButtonBehavior, HoverBehavior, BoxLayout):
    active = BooleanProperty(False)
    icon = StringProperty("android")
    icon_size = NumericProperty(30)
    hover_icon_color = ColorProperty([1, 1, 1, 1])
    normal_icon_color = ColorProperty([1, 1, 1, .3])
    tooltip_text = StringProperty("None")
    tooltip_bg_color = ListProperty([0, 0, 0, .6])
    tooltip_text_color = ListProperty((1, 1, 1, 1))
    tooltip_font_style = StringProperty()
    tooltip_radius = ListProperty([dp(7), ])

    _tooltip = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_state(self,  widget, value):
        #print(widget.tooltip_text,value)
        if value == "down":
            self.active = True
            _list = ToggleButtonBehavior.get_widgets('x')
            for each in _list:
                if each is not widget:
                    each.active = False
            del _list
            


    def on_enter(self):
        if(not self.active):
            self.ids.icon.text_color = self.hover_icon_color
        self._tooltip = MDTooltipViewClass(tooltip_bg_color=self.tooltip_bg_color,
                                           tooltip_text_color=self.tooltip_text_color,
                                           tooltip_text=self.tooltip_text,)
        self._tooltip.tooltip_font_style = self.tooltip_font_style,
        self._tooltip.tooltip_radius = self.tooltip_radius,
        Clock.schedule_once(self.display_tooltip, -1)

    def display_tooltip(self, interval):
        if not self._tooltip:
            return
        Window.add_widget(self._tooltip)
        pos = self.to_window(self.center_x, self.center_y)
        x = pos[0] + self.width / 2
        y = pos[1] - self.height / 2
        self._tooltip.pos = (x, y)
        Clock.schedule_once(self.animation_tooltip_show, 0)

    def animation_tooltip_show(self, interval):
        if not self._tooltip:
            return
        (
            Animation(_scale_x=1, _scale_y=1, d=0.1)
            + Animation(opacity=1, d=0.2)
        ).start(self._tooltip)

    def on_leave(self):
        if(not self.active):
            self.ids.icon.text_color = self.normal_icon_color
        if self._tooltip:
            Window.remove_widget(self._tooltip)
            self._tooltip = None
