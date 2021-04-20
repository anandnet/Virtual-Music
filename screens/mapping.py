from functools import partial
import json
import random
from widgets.dropitem import DropItem
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.uix.card import MDSeparator
from kivy.properties import (
    ListProperty,
    StringProperty,
)
from utils.selected_instrument import selected_instr
from utils.constant import instruments_items, finger_name
from utils.constant import clr


Builder.load_string("""
#:import DropItem widgets.dropitem 
<ListItem>:
    orientation:"vertical"
    size_hint_y:None
    height:"50dp"
    BoxLayout:
        BoxLayout:
            padding:20,0,0,0
            MDLabel:
                #theme_text_color:"Primary"
                color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                text:root.text
        BoxLayout:
            Widget:
            DropItem:
                size_hint_x:None
                width:"170dp"
                icon_color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                icon:"chevron-down"
                id: dropdown_item
                text: "None"
                transparent:True
                on_release: root.menu.open(self)
            Widget:

    MDSeparator:

<MusicMappingScreen>:
    BoxLayout:
        padding:80,20,20,20
        orientation:"vertical"
        canvas:
            Color:
                rgba:theme.get_color(app.theme_cls.theme_style,"BackgroundColor")
            Rectangle:
                pos:self.pos
                size:self.size
        BoxLayout:
            size_hint:None,None
            padding:20,0,0,0
            width:"250dp"
            height:"40dp"
            MDLabel:
                text:"Tune For"
                #theme_text_color:"Primary"
                color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                font_size:"18sp"
            DropItem:
                id:instr_drop
                size_hint_x:None
                icon_color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                width:"150dp"
                icon:"chevron-down"
                text: "Piano"
                transparent:True
                on_release: root.instrumentmenu.open(self)

        BoxLayout:
            size_hint_x:.5 if app.root.width>1000 else .7
            padding:"20dp"
            canvas:
                Color:
                    rgba:[0.1,0.1,0.1,1] if app.theme_cls.theme_style=="Dark" else [1,1,1,.8]
                RoundedRectangle:
                    pos:self.pos
                    size:self.size
            ScrollView:
                do_scroll_y: True
                BoxLayout:
                    size_hint_y:None
                    height: self.minimum_height
                    #canvas:
                    #    Color:
                    #        rgba:0.1,0.1,0.1,1
                    #    Rectangle:
                    #        pos:self.pos
                    #        size:self.size
                    orientation:"vertical"
                    BoxLayout:
                        size_hint_y:None
                        height:"60dp"
                        padding:5,0,0,0
                        MDLabel:
                            text:"Left Hand"
                            #theme_text_color:"Primary"
                            color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                            font_size:"23sp"
                            bold:True
                    MDSeparator:
                    BoxLayout:
                        id:lefthand
                        orientation:"vertical"
                        size_hint_y:None
                        height:self.minimum_height
                        
                    BoxLayout:
                        size_hint_y:None
                        height:"60dp"
                        MDLabel:
                            text:"Right Hand"
                            #theme_text_color:"Primary"
                            color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                            font_size:"23sp"
                            bold:True
                    MDSeparator:
                    BoxLayout:
                        id:righthand
                        orientation:"vertical"
                        size_hint_y:None
                        height:self.minimum_height
                        
                    
""")


class ListItem(BoxLayout):
    index = ListProperty()
    text = StringProperty()

    def __init__(self, selected_instr, finger_name, index, selected_text, notes, **kwargs):
        self.initial_selected_text = "None" if(
            selected_text == "") else selected_text
        self.text = finger_name
        self.index = index
        self.menu_items = notes
        self.selected_instr = selected_instr
        Clock.schedule_once(self.buildDropDown, 0)
        super(ListItem, self).__init__(**kwargs)

    def buildDropDown(self, args):
        self.ids.dropdown_item.text = self.initial_selected_text
        self.menu = DropDown()
        for each in self.menu_items:
            btn = DropItem(text=each.split(".")[0], icon="music-note",
                           icon_color=random.choice(clr))
            btn.bind(on_release=lambda btn: self.set_item(self.menu, btn))
            self.menu.add_widget(btn)
            self.menu.spacing = 0
            self.menu.add_widget(MDSeparator())

    def set_item(self, instance_menu, instance_menu_item):
        self.ids.dropdown_item.text = instance_menu_item.text
        import json
        with open('utils/map_data.json', 'r') as file:
            data = json.load(file)

        data[self.selected_instr][int(self.index[0])
                                  ][self.index[1]] = instance_menu_item.text

        with open('utils/map_data.json', 'w') as json_file:
            json.dump(data, json_file)
        instance_menu.dismiss()


class MusicMappingScreen(Screen):
    selected_instr = "piano"

    def __init__(self, **kwargs):
        Clock.schedule_once(self.buildDropDown, 0)
        super(MusicMappingScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        Clock.schedule_once(self.buildDropDown, 0)

    def buildDropDown(self, args):
        #Load All Notes
        with open('utils/notes.json', 'r') as file:
            self.music_notes = json.load(file)

        #check if select instr is available or not 
        from utils.selected_instrument import manual_instr
        if(self.selected_instr not in instruments_items+manual_instr):
            self.ids.instr_drop.text = "Piano"
            self.selected_instr = "piano"
        
        #build instr dropdown
        self.instrumentmenu = DropDown()
        for each in instruments_items+manual_instr:
            btn = DropItem(text=each.capitalize(), icon="piano")
            btn.bind(on_release=lambda btn: self.set_item(
                self.instrumentmenu, btn))
            self.instrumentmenu.add_widget(btn)
            self.instrumentmenu.spacing = 0
            self.instrumentmenu.add_widget(MDSeparator())
        self.add_mapping_table()

    def set_item(self, instance_menu, instance_menu_item):
        self.ids.instr_drop.text = instance_menu_item.text
        self.selected_instr = instance_menu_item.text.lower()
        instance_menu.dismiss()
        Clock.schedule_once(self.add_mapping_table)

    def add_mapping_table(self, *args):
        # print(self.music_notes[self.selected_instr])
        with open('utils/map_data.json', 'r') as file:
            mapped_data = json.load(file)
        lh_current_map = mapped_data[self.selected_instr][0]
        rh_current_map = mapped_data[self.selected_instr][1]
        # print("\n\nleft:",lh_current_map,"\n\nRight",rh_current_map)

        # building current mapped list for left hand
        if(len(self.ids.lefthand.children) > 0):
            self.ids.lefthand.clear_widgets()
        self.build_list(
            0, self.music_notes[self.selected_instr], lh_current_map)

        # building current mapped list for right hand
        if(len(self.ids.righthand.children) > 0):
            self.ids.righthand.clear_widgets()
        self.build_list(
            1, self.music_notes[self.selected_instr], rh_current_map)

    def build_list(self, hand_index, music_note, current_map):
        wid = self.ids.lefthand if(hand_index == 0) else self.ids.righthand

        for i in range(1, 6):
            wid.add_widget(ListItem(self.selected_instr, finger_name[i-1], [
                           str(hand_index), str(i)], current_map[str(i)], music_note))
