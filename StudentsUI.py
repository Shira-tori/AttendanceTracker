from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.graphics import Color
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivymd.uix.tab import MDTabsBase
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

class Tab(FloatLayout, MDTabsBase):
    pass


#class ScreenMan(ScreenManager):
#   pass
class ScreenMan(ScreenManager):
    pass

class StudentsUIApp(MDApp):
    def build(self):
        screenMan = ScreenMan()
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "Blue"
        #return Builder.load_file("StudentsUI.kv")
        return screenMan


if __name__ == '__main__':
    StudentsUIApp().run()