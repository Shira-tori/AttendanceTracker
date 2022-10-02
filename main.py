from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager

class ScreenMan(ScreenManager):
    pass

class AttendanceApp(MDApp):
    def build(self):
        screenMan = ScreenMan()
        self.theme_cls.theme_style = "Dark"
        return screenMan

if __name__ == '__main__':
    AttendanceApp().run()
