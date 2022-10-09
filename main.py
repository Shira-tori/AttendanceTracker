from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock
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
    grade = ObjectProperty()
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
        print("WRONG PASSWORD BITCH")
        return

    def login(self):
        try:
            mycursor.execute(f"SELECT lrn, password FROM students WHERE lrn = {int(self.lrn.text)}")
        except:
            anim = Animation(pos_hint={"center_y": .3}, d=.5, t='out_back')
            anim.start(self.signupButton)
            anim.start(self.loginButton)
            self.floatLayout.add_widget(MDLabel(text="LRN not found.", halign="center", pos_hint={"center_y": .36}, theme_text_color="Error"))
            return
        try:
            if self.password.text == mycursor.fetchone()[1]:
                print("Login Successful!")

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
                print("WRONG PASSWORD BITCH")
        except:
            self.error_anim()
            

    def register(self):
        if (self.fullname.error != True) and (self.section.error != True) and (self.lrn_register.error != True) and (self.password_register.error != True) and (self.grade.error != True) and (self.grade.text.isnumeric() == True) and (self.lrn_register.text.isnumeric() == True):
            mycursor.execute("INSERT INTO students (name, section, grade, lrn, password) VALUES (%s, %s, %s, %s ,%s)", (self.fullname.text.strip().upper(), self.section.text.strip().upper(), int(self.grade.text), int(self.lrn_register.text), self.password_register.text))
            mydb.commit()
            print(self.fullname.text.strip().upper(), self.section.text.strip().upper(), int(self.grade.text), int(self.lrn_register.text), self.password_register.text)
            print("SUCCESSFULLY CREATED AN ACCOUNT!")

    def update(self, dt):
        if (self.lrn.text.strip() == "") or (self.password.text.strip() == ""):
            self.loginButton.disabled = True
        else:
            self.loginButton.disabled = False

class AttendanceApp(MDApp):
    def build(self):
        screenMan = ScreenMan()
        self.theme_cls.theme_style = "Dark"
        Clock.schedule_interval(screenMan.update, 1.0/60.0)
        return screenMan

if __name__ == '__main__':
    AttendanceApp().run()
