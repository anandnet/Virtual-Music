from logging import root
from os import name
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from widgets.loader import Loader
from kivy.uix.behaviors import button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from screens.splash import SplashScreen


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Vitual Music"
        self.icon='assets/icons/app_icon.jpeg'
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette ="Purple"
        Clock.schedule_once(self.load_file, 5)
        self.manager = ScreenManager()
        splash_scr = SplashScreen(name="splash")
        self.manager.add_widget(splash_scr)
        self.root = self.manager

    def load_file(self, *args):
        a_pp = Builder.load_file("gui.kv")
        main_scr = Screen(name="main")
        main_scr.add_widget(a_pp)
        self.root.add_widget(main_scr)
        self.root.current = "main"


class Root(BoxLayout):
    pass


if __name__ == "__main__":
    MainApp().run()


"""
0.5,0.1,1,1
"""
