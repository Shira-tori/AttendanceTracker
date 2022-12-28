from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import CommonElevationBehavior
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

class BaseShadowMDCard(MDCard, CommonElevationBehavior):
    pass

class ScreenMan(ScreenManager):
    username = ObjectProperty()
    password = ObjectProperty()
    fullname = ObjectProperty()
    section = ObjectProperty()
    username_register = ObjectProperty()
    password_register = ObjectProperty()
    lrn_register = ObjectProperty()
    floatLayout = ObjectProperty()
    signupButton = ObjectProperty()
    loginButton = ObjectProperty()
    grade = ObjectProperty()
    students_ui = ObjectProperty()
    student_radio_button = ObjectProperty()
    teacher_radio_button = ObjectProperty()
    teachers_ui = ObjectProperty()
    strand_list_container = ObjectProperty()
    failed = BooleanProperty(False)
    def error_anim(self):
        if mycursor.fetchone() == None:
            if self.failed == True:
                self.floatLayout.remove_widget(self.floatLayout.children[0])
                self.floatLayout.add_widget(MDLabel(text="LRN not found.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
            else:
                anim = Animation(pos_hint={"center_y": .3}, d=.5, t='out_back')
                anim.start(self.signupButton)
                anim.start(self.loginButton)
                self.floatLayout.add_widget(MDLabel(text="LRN not found.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
                self.failed = True
            return
        if self.failed == True:
            self.floatLayout.remove_widget(self.floatLayout.children[0])
            self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
        else:
            anim = Animation(pos_hint={"center_y": .3}, d=.5, t='out_back')
            anim.start(self.signupButton)
            anim.start(self.loginButton)
            self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
            self.failed = True
        print("Incorrect password. Please try again.")
        return

    def login(self):
        try:
            print("LOGGING IN...")
            mycursor.execute(f'SELECT username, password FROM teachers_tbl WHERE username = "{self.username.text}"')
        except:
            anim = Animation(pos_hint={"center_y": .3}, d=.5, t='out_back')
            anim.start(self.signupButton)
            anim.start(self.loginButton)
            self.floatLayout.add_widget(MDLabel(text="LRN not found.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
            return
        try:
            if self.password.text == mycursor.fetchone()[1]:
                print("Login Successful!")
                self.current = "teachers_ui"

            else:
                if self.failed == True:
                    self.floatLayout.remove_widget(self.floatLayout.children[0])
                    self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
                else:
                    anim = Animation(pos_hint={"center_y": .3}, d=.5, t='out_back')
                    anim.start(self.signupButton)
                    anim.start(self.loginButton)
                    self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
                    self.failed = True
                print("Incorrect password. Please try again.")
        except:
            self.error_anim()
            

    def register(self):
        if (self.fullname.error != True) and (self.section.error != True) and (self.username_register.error != True) and (self.password_register.error != True) and (self.grade.error != True) and (self.grade.text.isnumeric() == True) and (self.lrn_register.text.isnumeric() == True):
            mycursor.execute("INSERT INTO students (name, username, section, grade, lrn, password) VALUES (%s, %s, %s, %s ,%s, %s)", (self.fullname.text.strip().upper(), self.username_register.text.strip(), self.section.text.strip().upper(), int(self.grade.text), int(self.lrn_register.text), self.password_register.text))
            mydb.commit()
            print(self.fullname.text.strip().upper(), self.username_register, self.section.text.strip().upper(), int(self.grade.text), int(self.lrn_register.text), self.password_register.text)
            print("SUCCESSFULLY CREATED AN ACCOUNT!")

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
