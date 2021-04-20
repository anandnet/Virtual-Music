from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
Builder.load_string("""
#:import theme utils.theme
<SplashScreen>:
    BoxLayout:
        canvas:
            Color:
                rgba:theme.get_color(app.theme_cls.theme_style,"BackgroundColor")
            Rectangle:
                pos:self.pos
                size:self.size

        orientation:"vertical"
        BoxLayout:
            size_hint_y:.20
            
        BoxLayout:
            size_hint_y:.55
            AnchorLayout:
                Image:
                    size_hint_y:1
                    source:'assets/icons/treble-clef 12.png'
        
        BoxLayout:
            size_hint_y:.25
            AnchorLayout:
                Loader:
                    size_hint_x:None
                    width:"400dp"
                    bg_color:[0.7,.7,.7,1]
                    fill_color:theme.get_color(app.theme_cls.theme_style,"ThemeColor")
                    value:0
            
""")
class SplashScreen(Screen):
    pass