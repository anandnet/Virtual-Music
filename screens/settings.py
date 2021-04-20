
import os
import shutil
from functools import partial
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.dropdown import DropDown
from kivymd.uix.card import MDSeparator
from widgets.dropitem import DropItem
from plyer import filechooser
from utils.refresh_notes import refresh
Builder.load_string("""
<InstrumentList>:
    size_hint_y:None
    height:"50dp"
    padding:15,0,15,0
    canvas:
        Color:
            rgba:(1,1,1,.5) if app.theme_cls.theme_style=="Dark" else (0,0,0,.5)
        RoundedRectangle:
            pos:self.pos
            size:self.size
    MDLabel:
        text:root.text
    MDIconButton:
        icon:"delete"
        on_release:root.remove_instrument(root.parent)

<AddInstrumentBox>:
    size_hint_y:None
    height:"220dp"
    orientation:"vertical"
    padding:"10dp"
    
    MDTextField:
        size_hint_y:None
        height:"40dp"
        id:instrumentname
        hint_text: "Instrument Name"
        
    BoxLayout:
        size_hint_y:None
        height:"40dp"
        MDLabel:
            text:"Select Folder"
            color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
        MDIconButton:
            icon:"folder-plus-outline"
            on_release:root.select_folder()
    MDLabel:
        size_hint_y:None
        height:"10dp" if self.text=="" else "40dp" 
        id:path
        text:""
        color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
        font_size:"12sp"
    MDLabel:
        size_hint_y:None
        height:"1dp" if self.text=="" else "30dp"
        id:warning
        text:""
        color:(1,0,0,1)
        font_size:"12sp"
    FloatLayout:
        MDRaisedButton:
            text:"Cancel"
            pos_hint: {"x":0.35, "center_y":0.4}
            on_release:root.remove_self(root.parent)
        MDRaisedButton:
            text:"Add"
            pos_hint:{"x":.65,"center_y":0.4}
            on_release:root.add_instrument(root.parent)

<SettingScreen>:
    #Backgroud
    BoxLayout:
        orientation:"vertical"
        canvas:
            Color:
                rgba:theme.get_color(app.theme_cls.theme_style,"BackgroundColor")
            Rectangle:
                pos:self.pos
                size:self.size
        
        ScrollView:
            do_scroll_x:True
            BoxLayout:
                size_hint_x:None
                width: self.minimum_width+80
                spacing:"40dp"
                padding: 30 ,20,0,root.height-430
                # Genral Setting
                BoxLayout:
                    orientation:"vertical"
                    size_hint:None,None
                    height:"400dp"
                    width:"400dp"
                    padding:"30dp"
                    canvas:
                        Color:
                            rgba:[0.15,0.15,0.15,1] if app.theme_cls.theme_style=="Dark" else [1,1,1,.8]
                        RoundedRectangle:
                            pos:self.pos
                            size:self.size
                    MDLabel:
                        size_hint_y:None
                        height:"50dp"
                        text:"General"
                        font_size:"20sp"
                        color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                    MDSeparator:
                    #Dark Mode
                    BoxLayout:
                        size_hint_y:None
                        height:"40dp"
                        padding:10,0,10,0
                        MDLabel:
                            text:"Dark Mode"
                            color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                        MDSwitch:
                            size_hint:(None,None)
                            height:"40dp"
                            width:"40dp"
                            active: True if app.theme_cls.theme_style=="Dark" else False
                            on_active:
                                app.theme_cls.theme_style="Dark" if self.active\
                                else "Light"
                    MDSeparator:
                    BoxLayout:
                        size_hint_y:None
                        height:"40dp"
                        padding:10,0,0,0
                        MDLabel:
                            text:"Camera"
                            color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                        DropItem:
                            size_hint_x:None
                            width:"180dp" if len(self.text)>8 else "150dp" if len(self.text)>4 else "130dp"
                            id:dropdown_item
                            transparent:True
                            text:"Default"
                            icon:"chevron-down"
                            font_size:"12sp" if len(self.text)>10 else "14sp"
                            on_release:root.open_camera_list(self)
                        
                    Widget:
                # Add Additional instrument
                BoxLayout:
                    orientation:"vertical"
                    size_hint:None,None
                    height:"400dp"
                    width:"400dp"
                    padding:"30dp"
                    canvas:
                        Color:
                            rgba:[0.15,0.15,0.15,1] if app.theme_cls.theme_style=="Dark" else [1,1,1,.8]
                        RoundedRectangle:
                            pos:self.pos
                            size:self.size
                    BoxLayout:
                        orientation:"vertical"
                        BoxLayout:
                            size_hint_y:None
                            height:"40dp"
                            MDLabel:
                                size_hint_y:None
                                height:"50dp"
                                text:"Add Instrument"
                                font_size:"20sp"
                                color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                            MDIconButton:
                                icon:"plus"
                                on_release:root.add_box(root.ids.instaddbox)
                        MDSeparator:
                        Widget:
                            size_hint_y:None
                            height:"2dp"
                        ScrollView:
                            do_scroll_y:True
                            BoxLayout:
                                id:wholebox
                                spacing:"5dp"
                                size_hint_y:None
                                height:self.minimum_height
                                orientation:"vertical"
                                BoxLayout:
                                    id:instaddbox
                                    size_hint_y:None
                                    height:"0dp"
                                    canvas:
                                        Color:
                                            rgba:1,0,1,.15
                                        RoundedRectangle:
                                            pos:self.pos
                                            size:self.size                
                    
        Widget:
            size_hint_y:None
            height:"2dp"
            
            
""")


class InstrumentList(BoxLayout):
    text = StringProperty()

    def __init__(self, text, **kwargs):
        self.text = text
        super(InstrumentList, self).__init__(**kwargs)

    def remove_instrument(self, parent_wid):
        # remove dir folder
        shutil.rmtree("assets/tones/"+self.text.lower(), ignore_errors=True)
        # os.rmdir(os.path.abspath("assets/tones/"+self.text))

        # remove from manual_instr list
        import utils.selected_instrument as ut
        ut.manual_instr.remove(self.text.lower())
        st = "selected_instr = '{}'\ncamera_indx = {}\nmanual_instr = {}".format(
            ut.selected_instr, ut.camera_indx, ut.manual_instr)

        with open('utils/selected_instrument.py', 'w') as file:
            file.write(st)

        # remove from notes.json
        refresh()

        # remove from map_data.json
        import json
        with open('utils/map_data.json', 'r') as file:
            data = json.load(file)

        data.pop(self.text.lower())

        with open('utils/map_data.json', 'w') as json_file:
            json.dump(data, json_file)

        parent_wid.remove_widget(self)


class AddInstrumentBox(BoxLayout):

    def add_instrument(self, parent_wid):
        self.ids.warning.text = ""
        name = self.ids.instrumentname.text.rstrip().lower()
        path = self.ids.path.text
        from utils.selected_instrument import manual_instr
        from utils.constant import instruments_items
        if(name != ''):
            if(name not in manual_instr+instruments_items):
                if(path != ''):
                    files = [each for each in os.listdir(path) if each.split(
                        ".")[-1].lower() in ['wav', 'ogg']]
                    print(files)
                    if(files != []):
                        if(not os.path.exists("assets/tones/"+name)):
                            os.mkdir("assets/tones/"+name)

                        # copying all the assets to program folder
                        for file in files:
                            if os.path.isfile(os.path.join(path, file)):
                                shutil.copyfile(os.path.join(path, file), os.path.join(
                                    os.path.abspath("assets/tones/"+name), file))

                        # Set instrument which is manually added,to file
                        import utils.selected_instrument as ut
                        ut.manual_instr.append(name)
                        st = "selected_instr = '{}'\ncamera_indx = {}\nmanual_instr = {}".format(
                            ut.selected_instr, ut.camera_indx, ut.manual_instr)

                        with open('utils/selected_instrument.py', 'w') as file:
                            file.write(st)

                        # refresh notes.json
                        refresh()

                        #add in map_data.json
                        import json
                        with open('utils/map_data.json', 'r') as file:
                            data = json.load(file)

                        data[name] = [{"1": "", "2": "", "3": "", "4": "", "5": ""}, {
                            "1": "", "2": "", "3": "", "4": "", "5": ""}]

                        with open('utils/map_data.json', 'w') as json_file:
                            json.dump(data, json_file)

                        self.remove_self(parent_wid)
                        Clock.schedule_once(partial(
                            self.add_instr_to_list, parent_wid, InstrumentList(name.capitalize())), .6)

                    else:
                        self.ids.warning.text = "No file found with ext .wav,.ogg"
                else:
                    self.ids.warning.text = "! Folder Not Selected"
            else:
                self.ids.warning.text = "! Name already taken"
        else:
            self.ids.warning.text = "! Instrument Name left blank"

    def add_instr_to_list(self, parent_wid, list_widget, *args):
        """
        this function creted only for delay
        """
        parent_wid.parent.add_widget(list_widget)

    def select_folder(self):
        path = filechooser.choose_dir(title="Select Instrument Folder")
        if(path != []):
            self.ids.path.text = path[0]

    def remove_self(self, parent_wid):
        parent_wid.remove_widget(self)
        anim = Animation(height=0,
                         duration=.5
                         )
        anim.start(parent_wid)


class SettingScreen(Screen):
    def __init__(self, **kw):
        Clock.schedule_once(self.set_camera)
        Clock.schedule_once(self.build_instr_list)
        super(SettingScreen, self).__init__(**kw)

    def build_instr_list(self, *args):
        from utils.selected_instrument import manual_instr
        for each in manual_instr:
            self.ids.wholebox.add_widget(InstrumentList(each.capitalize()))

    def set_camera(self, *args):
        from utils.selected_instrument import camera_indx
        try:
            from pygrabber.dshow_graph import FilterGraph
            self.ids.dropdown_item.text = FilterGraph().get_input_devices()[
                camera_indx]
        except:
            pass

    def open_camera_list(self, inst):
        menu = DropDown(auto_width=False, width=200)
        try:
            from pygrabber.dshow_graph import FilterGraph
            device_list = FilterGraph().get_input_devices()
        except:
            device_list = []
        for i, each in enumerate(device_list):
            btn = DropItem(text=each, icon="webcam", font_size=15)
            btn.camera_indx = i
            btn.bind(on_release=lambda btn: self.set_item(menu, btn))
            menu.add_widget(btn)
            menu.spacing = 0
            menu.add_widget(MDSeparator())
        menu.open(inst)

    def set_item(self, dropdown, selected_btn):
        self.ids.dropdown_item.text = selected_btn.text
        import utils.selected_instrument as ut
        ut.camera_indx = selected_btn.camera_indx

        st = "selected_instr = '{}'\ncamera_indx = {}\nmanual_instr = {}".format(
            ut.selected_instr, selected_btn.camera_indx, ut.manual_instr)

        with open('utils/selected_instrument.py', 'w') as file:
            file.write(st)
        dropdown.dismiss()

    def add_box(self, inst):
        if(len(inst.children) == 0):
            anim = Animation(height=220,
                             duration=.5
                             )
            anim.start(inst)
            Clock.schedule_once(partial(self.add, inst), .5)

    def add(self, inst, *args):
        if(len(inst.children) == 0):
            inst.add_widget(AddInstrumentBox())
