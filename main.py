from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock

import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="pr2",
        port=3306
    )

mycursor = mydb.cursor()

class Tab(MDFloatLayout, MDTabsBase):
    pass

class ScreenMan(ScreenManager):
    username = ObjectProperty()
    password = ObjectProperty()
    floatLayout = ObjectProperty()
    loginButton = ObjectProperty()
    students_ui = ObjectProperty()
    student_radio_button = ObjectProperty()
    teacher_radio_button = ObjectProperty()
    teachers_ui = ObjectProperty()
    strand_list_container = ObjectProperty()
    failed = BooleanProperty(False)
    def login(self):
        print("LOGGING IN...")
        mycursor.execute(f'SELECT username, password FROM teachers_tbl WHERE username = "{self.username.text}"')
        if mycursor.fetchone() == None:
            if self.failed == False:
                anim = Animation(pos_hint={"center_y": .3}, d=.5, t='out_back')
                anim.start(self.loginButton)
                self.floatLayout.add_widget(MDLabel(text="Username not found. Please try again", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
                self.failed = True
                return
            else:
                self.floatLayout.remove_widget(self.floatLayout.children[0])
                self.floatLayout.add_widget(MDLabel(text="Username not found. Please try again", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
                return
        #TO DO: gawan ng code ung sa student na login
        mycursor.execute(f'SELECT username, password FROM teachers_tbl WHERE username = "{self.username.text}"')
        if self.password.text == mycursor.fetchone()[1]:
            print("Login Successful!")
            self.current = "teachers_ui"

        else:
            if self.failed == True:
                self.floatLayout.remove_widget(self.floatLayout.children[0])
                self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
            else:
                if self.failed == False:
                    anim = Animation(pos_hint={"center_y": .3}, d=.5, t='out_back')
                    anim.start(self.loginButton)
                    self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
                    self.failed = True
                    print("Incorrect password. Please try again.")
                else:
                    self.floatLayout.remove_widget(self.floatLayout.children[0])
                    self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
                    return
            
    def update(self, dt):
        if (self.username.text.strip() == "") or (self.password.text.strip() == ""):
            self.loginButton.disabled = True
        else:
            self.loginButton.disabled = False

class AttendanceApp(MDApp):
    def build(self):
        screenMan = ScreenMan()
        #self.theme_cls.theme_style = "Dark"
        Clock.schedule_interval(screenMan.update, 1.0/60.0)
        return screenMan

if __name__ == '__main__':
    AttendanceApp().run()
