from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.animation import Animation, AnimationTransition
from kivy_garden.zbarcam import ZBarCam
from kivy.clock import Clock

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="pr2",
    port=3306
)

mycursor = mydb.cursor(buffered=True)


class Tab(MDFloatLayout, MDTabsBase):
    pass


class LoginScreen(Screen):
    username = ObjectProperty()
    password = ObjectProperty()
    floatLayout = ObjectProperty()
    loginButton = ObjectProperty()
    students_ui = ObjectProperty()
    student_radio_button = ObjectProperty()
    teacher_radio_button = ObjectProperty()
    teachers_ui = ObjectProperty()
    strand_list_container = ObjectProperty()
    zbarcam = ObjectProperty(None)
    failed = BooleanProperty(False)

    def login(self):
        print("LOGGING IN...")
        if self.teacher_radio_button.active == True:
            mycursor.execute(
                f'SELECT username, password FROM teachers_tbl WHERE username = "{self.username.text}"')
            if mycursor.fetchone() == None:
                if self.failed == False:
                    anim = Animation(
                        pos_hint={"center_y": .3}, d=.5, t='out_back')
                    anim.start(self.loginButton)
                    self.floatLayout.add_widget(MDLabel(text="Username not found. Please try again", halign="center", pos_hint={
                                                "center_y": .36}, theme_text_color="Error"))
                    self.failed = True
                    return
                else:
                    self.floatLayout.remove_widget(
                        self.floatLayout.children[0])
                    self.floatLayout.add_widget(MDLabel(text="Username not found. Please try again", halign="center", pos_hint={
                                                "center_y": .36}, theme_text_color="Error"))
                    return
            mycursor.execute(
                f'SELECT username, password FROM teachers_tbl WHERE username = "{self.username.text}"')
            if self.password.text == mycursor.fetchone()[1]:
                print("Login Successful!")
                self.parent.add_widget(TeachersUI())
                self.parent.switch_to(
                    self.parent.screens[len(self.parent.screens) - 1])
            else:
                if self.failed == True:
                    self.floatLayout.remove_widget(
                        self.floatLayout.children[0])
                    self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={
                                                "center_y": .36}, theme_text_color="Error"))
                else:
                    if self.failed == False:
                        anim = Animation(
                            pos_hint={"center_y": .3}, d=.5, t='out_back')
                        anim.start(self.loginButton)
                        self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={
                                                    "center_y": .36}, theme_text_color="Error"))
                        self.failed = True
                        print("Incorrect password. Please try again.")
                    else:
                        self.floatLayout.remove_widget(
                            self.floatLayout.children[0])
                        self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={
                                                    "center_y": .36}, theme_text_color="Error"))
                        return
        else:
            mycursor.execute(
                f'SELECT username, password FROM students_account_tbl WHERE username = "{self.username.text}"')
            if mycursor.fetchone() == None:
                if self.failed == False:
                    anim = Animation(
                        pos_hint={"center_y": .3}, d=.5, t='out_back')
                    anim.start(self.loginButton)
                    self.floatLayout.add_widget(MDLabel(text="Username not found. Please try again", halign="center", pos_hint={
                                                "center_y": .36}, theme_text_color="Error"))
                    self.failed = True
                    return
                else:
                    self.floatLayout.remove_widget(
                        self.floatLayout.children[0])
                    self.floatLayout.add_widget(MDLabel(text="Username not found. Please try again", halign="center", pos_hint={
                                                "center_y": .36}, theme_text_color="Error"))
                    return
            mycursor.execute(
                f'SELECT username, password FROM students_account_tbl WHERE username = "{self.username.text}"')
            for x in mycursor.fetchall():
                if self.password.text == x[1]:
                    print("Login Successful!")
                    self.parent.switch_to(
                        self.parent.screens[len(self.parent.screens) - 1])
                    break

            else:
                if self.failed == True:
                    self.floatLayout.remove_widget(
                        self.floatLayout.children[0])
                    self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={
                                                "center_y": .36}, theme_text_color="Error"))
                else:
                    if self.failed == False:
                        anim = Animation(
                            pos_hint={"center_y": .3}, d=.5, t='out_back')
                        anim.start(self.loginButton)
                        self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={
                                                    "center_y": .36}, theme_text_color="Error"))
                        self.failed = True
                        print("Incorrect password. Please try again.")
                    else:
                        self.floatLayout.remove_widget(
                            self.floatLayout.children[0])
                        self.floatLayout.add_widget(MDLabel(text="Incorrect password. Please try again.", halign="center", pos_hint={
                                                    "center_y": .36}, theme_text_color="Error"))
                        return

    def update(self, dt):
        if (self.username.text.strip() == "") or (self.password.text.strip() == ""):
            self.loginButton.disabled = True
        else:
            self.loginButton.disabled = False


class StudentsUI(Screen):
    zbarcam = ObjectProperty(None)

    def init_zbarcam(self):
        if not self.zbarcam:
            self.zbarcam = ZBarCam()
            self.ids['scanner_boxlayout'].add_widget(self.zbarcam)
            self.ids['students_screen_man'].switch_to(
                self.ids['students_ui_scanner'])
            Clock.schedule_interval(self.scanning_qr, 1)
        else:
            self.ids['students_screen_man'].switch_to(
                self.ids['students_ui_scanner'], direction='left')
            self.zbarcam.xcamera._camera.init_camera()
            self.zbarcam.start()
            Clock.schedule_interval(self.scanning_qr, 1)
            return

    def scanning_qr(self, time):
        if self.zbarcam.symbols:
            print(self.zbarcam.symbols[0].data.decode())


class TeachersUI(Screen):
    pass


class ScreenMan(ScreenManager):
    pass


class AttendanceApp(MDApp):
    def build(self):
        screenMan = ScreenMan()
        login_screen = LoginScreen()
        # self.theme_cls.theme_style = "Dark"
        Clock.schedule_interval(login_screen.update, 1.0/60.0)
        return screenMan


if __name__ == '__main__':
    AttendanceApp().run()
