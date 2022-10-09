from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.graphics import Color
from kivy.uix.label import Label
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivymd.uix.tab import MDTabsBase
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

class NavLayout(MDNavigationLayout):
    pass

class Tab(FloatLayout, MDTabsBase):
    pass

class MainScreen(MDScreen):
    pass

class ScreenMan(ScreenManager):
    pass

class TEACHERSACC(MDApp):
    def build(self):
        mainScreen = MainScreen()
        navlayout = NavLayout()
        screenMan = ScreenMan()
        mainScreen.add_widget(navlayout)
        return mainScreen


if __name__ == '__main__':
    TEACHERSACC().run()

