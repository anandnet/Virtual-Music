from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
Builder.load_string("""
<HelpHeading@BoxLayout>:


<HelpScreen>:
    BoxLayout:
        padding:25
        orientation:"vertical"
        canvas:
            Color:
                rgba:theme.get_color(app.theme_cls.theme_style,"BackgroundColor")
            Rectangle:
                pos:self.pos
                size:self.size
        BoxLayout:
            orientation:"vertical"
            size_hint_y:None
            height:"40dp"
            MDLabel:
                text:"Help"
                font_size:"30sp"
                color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
            MDSeparator:
        ScrollView:
            
            BoxLayout:
                size_hint_y:None
                height:self.minimum_height
                orientation:"vertical"
                Widget:
                    size_hint_y:None
                    height:"30dp"
                BoxLayout:
                    orientation:"vertical"
                    size_hint_y:None
                    height:"120dp"
                    MDLabel:
                        color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                        text:"* How to Play instrument?"
                        font_size:"18sp"
                    MDLabel:
                        color:theme.get_color(app.theme_cls.theme_style,"SecondaryTextColor")
                        font_size:"14sp"
                        text:"Go to Home Screen \\n >> Select Instrument you want to play \\n >> No tune will be played if all fingers are in up direction\\n >> Finger which is down the mapped tune with that finger will be played"
                Widget:
                    size_hint_y:None
                    height:"30dp"
                BoxLayout:
                    orientation:"vertical"
                    size_hint_y:None
                    height:"90dp"
                    MDLabel:
                        color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                        text:"* How to map instrument notes?"
                        font_size:"18sp"
                    MDLabel:
                        color:theme.get_color(app.theme_cls.theme_style,"SecondaryTextColor")
                        font_size:"14sp"
                        text:"Go to Mapping screen \\n  >> Select instrument dropdown available nearby tune for\\n  >> All current tunes will apear for right hand and left hand fingers\\n  >> Now tune can be selected for all fingers in both hand"
                Widget:
                    size_hint_y:None
                    height:"30dp"
                BoxLayout:
                    orientation:"vertical"
                    size_hint_y:None
                    height:"120dp"
                    MDLabel:
                        color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                        text:"* How to Change Camera?"
                        font_size:"18sp"
                    MDLabel:
                        color:theme.get_color(app.theme_cls.theme_style,"SecondaryTextColor")
                        font_size:"14sp"
                        text:"Go to setting screen \\n  >> Go to the Section Genral\\n  >>Click on dropdown dropdown available in right of camera\\n  >> A camera list will apear then select your camera\\n  >> This feature is limited for windows platform only"
                Widget:
                    size_hint_y:None
                    height:"30dp"
                BoxLayout:
                    orientation:"vertical"
                    size_hint_y:None
                    height:"120dp"
                    MDLabel:
                        color:theme.get_color(app.theme_cls.theme_style,"PrimaryTextColor")
                        text:"* How to add new Instrument?"
                        font_size:"18sp"
                    MDLabel:
                        color:theme.get_color(app.theme_cls.theme_style,"SecondaryTextColor")
                        font_size:"14sp"
                        text:"Go to setting screen \\n  >> Go to the Section Add Instrument\\n  >> Click on '+' icon \\n  >> A Layout will apear fill instrument name,select tune directory and  hit add button\\n  >> voila! instrument will be added"
                    

            
        
""")
class HelpScreen(Screen):
    pass