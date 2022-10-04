from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivy.properties import ObjectProperty
from kivy.animation import Animation, AnimationTransition
import mysql.connector

mydb = mysql.connector.connect(
        host="sql6.freemysqlhosting.net",
        user="sql6523636",
        passwd="YQIBTXeknU",
        database="sql6523636",
        port=3306
    )

mycursor = mydb.cursor()

class ScreenMan(ScreenManager):
    lrn = ObjectProperty()
    password = ObjectProperty()
    fullname = ObjectProperty()
    section = ObjectProperty()
    lrn_register = ObjectProperty()
    password_register = ObjectProperty()
    floatLayout = ObjectProperty()
    signupButton = ObjectProperty()
    loginButton = ObjectProperty()
    def login(self):
        try:
            mycursor.execute("SELECT lrn, password FROM students WHERE lrn = {}".format(int(self.lrn.text)))
        except:
            print("LRN not found")
            anim = Animation(pos_hint={"center_y": .3}, d=.5, t=AnimationTransition.in_back(1))
            anim.start(self.signupButton)
            anim.start(self.loginButton)
            anim.on_complete(self.floatLayout.add_widget(MDLabel(text="LRN not found", halign="center", pos_hint={"center_y": .36})))
            return
        if self.password.text == mycursor.fetchone()[1]:
            print("Login Successful!")
        else:
            print("WRONG PASSWORD BITCH")

    def register(self):
        if (self.fullname.error != True) and (self.section.error != True) and (self.lrn_register.error != True) and (self.password_register != True):
            mycursor.execute("INSERT INTO students (name, section, grade, lrn, password) VALUES (%s, %s, %s, %s ,%s)", (self.fullname.text, self.section.text, "8", self.lrn_register.text, self.password_register.text))


class AttendanceApp(MDApp):
    def build(self):
        screenMan = ScreenMan()
        self.theme_cls.theme_style = "Dark"
        return screenMan

if __name__ == '__main__':
    AttendanceApp().run()
