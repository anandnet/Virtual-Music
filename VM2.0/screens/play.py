from widgets.dropitem import DropItem
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock
from kivymd.uix.card import MDSeparator
from kivy.properties import (
    ListProperty,
)
from utils.selected_instrument import inst_indx
import json
Builder.load_string("""
#:import DropItem widgets.dropitem 
<ListItem>:
    orientation:"vertical"
    size_hint_y:None
    height:50
    text:""
    BoxLayout:
        BoxLayout:
            padding:20,0,0,0
            MDLabel:
                theme_text_color:"Primary"
                text:root.text
        BoxLayout:
            Widget:
            DropItem:
                size_hint_x:None
                width:170
                icon:"chevron-down"
                id: dropdown_item
                text: "None"
                transparent:True
                on_release: root.menu.open(self)
            Widget:

    MDSeparator:

<PlayScreen>:
    ScrollView:
        do_scroll_y: True
        BoxLayout:
            size_hint_y:None
            height: self.minimum_height
            canvas:
                Color:
                    rgba:0.1,0.1,0.1,1
                Rectangle:
                    pos:self.pos
                    size:self.size
            orientation:"vertical"
            BoxLayout:
                size_hint_y:None
                height:60
                padding:5,0,0,0
                MDLabel:
                    text:"Left Hand"
                    theme_text_color:"Primary"
                    font_size:35
            MDSeparator:
            ListItem:
                text:"Thumb"
                index:(["0","1"])
            ListItem:
                text:"Index Finger"
                index:(["0","2"])
            ListItem:
                text:"Middle Finger"
                index:(["0","3"])
            ListItem:
                text:"Ring Finger"
                index:(["0","4"])
            ListItem:
                text:"Little Finger"
                index:(["0","5"])

            BoxLayout:
                size_hint_y:None
                height:60
                MDLabel:
                    text:"Right Hand"
                    theme_text_color:"Primary"
                    font_size:35
            MDSeparator:
            ListItem:
                text:"Thumb"
                index:(["1","1"])
            ListItem:
                text:"Index Finger"
                index:(["1","2"])
            ListItem:
                text:"Middle Finger"
                index:(["1","3"])
            ListItem:
                text:"Ring Finger"
                index:(["1","4"])
            ListItem:
                text:"Little Finger"
                index:(["1","5"])
            Widget:




""")


class ListItem(BoxLayout):
    index = ListProperty()

    def __init__(self, **kwargs):
        Clock.schedule_once(self.buildDropDown, 0)
        super(ListItem, self).__init__(**kwargs)

    def buildDropDown(self, args):
        with open('utils/notes.json', 'r') as file:
            menu_items = json.load(file)[str(inst_indx)]

        self.menu = DropDown()
        for each in menu_items:
            btn = DropItem(text=each,icon="music-note")
            btn.bind(on_release=lambda btn: self.set_item(self.menu, btn))
            self.menu.add_widget(btn)
            self.menu.spacing=0
            self.menu.add_widget(MDSeparator())

    def set_item(self, instance_menu, instance_menu_item):
        self.ids.dropdown_item.text = instance_menu_item.text
        import json
        with open('utils/map_data.json', 'r') as file:
            data = json.load(file)

        data[str(inst_indx)][int(self.index[0])
                     ][self.index[1]] = instance_menu_item.text

        with open('utils/map_data.json', 'w') as json_file:
            json.dump(data, json_file)
        instance_menu.dismiss()


class PlayScreen(Screen):
    pass
