from os import name
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.behaviors import button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
import datetime

colors = {
    "Teal": {
        "50": "e4f8f9",
        "100": "bdedf0",
        "200": "97e2e8",
        "300": "79d5de",
        "400": "6dcbd6",
        "500": "6ac2cf",
        "600": "63b2bc",
        "700": "5b9ca3",
        "800": "54888c",
        "900": "486363",
        "A100": "bdedf0",
        "A200": "97e2e8",
        "A400": "6dcbd6",
        "A700": "5b9ca3",
    },
    "Blue": {
        "50": "e3f3f8",
        "100": "b9e1ee",
        "200": "91cee3",
        "300": "72bad6",
        "400": "62acce",
        "500": "589fc6",
        "600": "5191b8",
        "700": "487fa5",
        "800": "426f91",
        "900": "35506d",
        "A100": "b9e1ee",
        "A200": "91cee3",
        "A400": "62acce",
        "A700": "487fa5",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "F5F5F5",
        "Background": "FAFAFA",
        "CardsDialogs": "FFFFFF",
        "FlatButtonDown": "cccccc",
    },
    "Dark": {
        "StatusBar": "000000",
        "AppBar": "212121",
        "Background": "303030",
        "CardsDialogs": "424242",
        "FlatButtonDown": "999999",
    }
}


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Vitual Music"
        super().__init__(**kwargs)

    def build(self):
        Clock.schedule_once(self.load_file, 5)
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        self.manager = ScreenManager()
        splash_scr = Screen(name="splash")

        img = Image(source='assets/icons/music.png', pos=(800, 800))
        animation = Animation(x=0, y=0, d=4, t="out_bounce")
        animation.start(img)
        splash_scr.add_widget(img)
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
