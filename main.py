import qrcode
import os
import datetime
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import OneLineListItem
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import FallOutTransition
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.animation import Animation, AnimationTransition
from kivy_garden.zbarcam import ZBarCam
from kivy.clock import Clock
from kivy.core.window import Window
from kivy_garden.xcamera.platform_api import PORTRAIT, set_orientation

import mysql.connector

Window.size = (360, 640)

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
                f'SELECT username, password, teacher_Id FROM teachers_tbl WHERE username = "{self.username.text}"')
            teacher = mycursor.fetchone()
            if self.password.text == teacher[1]:
                print("Login Successful!")
                global TEACHERS_ID
                TEACHERS_ID = teacher[2]
                self.parent.login_teachers()
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
                f'SELECT username, password, fullname FROM students_account_tbl WHERE username = "{self.username.text}"')
            for x in mycursor.fetchall():
                if self.password.text == x[1]:
                    print("Login Successful!")
                    global STUDENT_FULLNAME
                    STUDENT_FULLNAME = x[2]
                    print(x[2])
                    self.parent.login_students()
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
            data = self.zbarcam.symbols[0].data.decode()
            try:
                data = data.split(":")

            except:
                print("Error")

            if data[1] == "HATDOG":
                global STUDENT_FULLNAME
                now = datetime.datetime.now()
                date = now.strftime("%Y-%m-%d")
                fullname = STUDENT_FULLNAME.strip("\n")
                print(fullname)
                mycursor.execute(
                    f'SELECT student_id FROM students_tbl WHERE name = "{STUDENT_FULLNAME}"')
                student_id = mycursor.fetchone()
                print(student_id)
                mycursor.execute(
                    "INSERT INTO attendance_tbl (date, student_id) VALUES (%s, %s)", (date, student_id[0]))
                mydb.commit()

    def check_tabs(self):
        if self.ids["students_ui_tabs"].get_current_tab() == self.ids["qr_code_tab"]:
            if len(self.ids["qr_scanner_tab_boxlayout"].children) == 0:
                zbar = ZBarCam()
                self.ids["qr_scanner_tab_boxlayout"].add_widget(zbar)
                self.zbarcam = zbar
                Clock.schedule_interval(self.scanning_qr, 1)
            else:
                self.ids["qr_scanner_tab_boxlayout"].children[0].start()
                self.ids["qr_scanner_tab_boxlayout"].children[0].xcamera._camera.init_camera()
                self.ids["qr_scanner_tab_boxlayout"].children[0].xcamera.resolution = (
                    360, 640)
                Clock.schedule_interval(self.scanning_qr, 1)

        else:
            if len(self.ids["qr_scanner_tab_boxlayout"].children) != 0:
                self.ids["qr_scanner_tab_boxlayout"].children[0].stop()
                self.ids["qr_scanner_tab_boxlayout"].children[0].xcamera._camera._device.release(
                )
                Clock.unschedule(self.scanning_qr, 1)


class TeachersUI(Screen):
    def section_list(self):
        global TEACHERS_ID
        self.ids["teachers_ui_screen_manager"].switch_to(
            self.ids["teachers_ui_section_list"], direction='left')
        mycursor.execute(
            f"SELECT * FROM strands_tbl WHERE teachers_Id = {TEACHERS_ID}")
        print(len(self.ids["teachers_ui_section_list_container"].children))
        if len(self.ids["teachers_ui_section_list_container"].children) == 0:
            for x in mycursor.fetchall():
                self.ids["teachers_ui_section_list_container"].add_widget(
                    OneLineListItem(text=x[0]))


class ScreenMan(ScreenManager):
    def logout(self):
        self.add_widget(LoginScreen())
        self.current = "login_screen"
        if os.path.isfile("qrcode.png"):
            os.remove("qrcode.png")
        Clock.schedule_once(self.debug, .5)

    def login_students(self):
        global STUDENT_FULLNAME
        print(STUDENT_FULLNAME)
        if STUDENT_FULLNAME:
            qrcode_img = qrcode.make(STUDENT_FULLNAME + ":HATDOG")
            print(STUDENT_FULLNAME)
            type(qrcode_img)
            qrcode_img.save("qrcode.png")
        self.add_widget(StudentsUI())
        self.current = "students_ui"
        Clock.schedule_once(self.debug, .5)

    def login_teachers(self):
        self.add_widget(TeachersUI())
        self.current = "teachers_ui"
        Clock.schedule_once(self.debug, .5)

    def debug(self, dt):
        print(self.screens)
        self.remove_widget(self.screens[0])
        print(self.screens)


class AttendanceApp(MDApp):
    login_screen = ObjectProperty()

    def build(self):
        screenMan = ScreenMan(transition=FallOutTransition())
        login_screen = LoginScreen()
        self.login_screen = login_screen
        screenMan.add_widget(login_screen)
        Clock.schedule_interval(login_screen.update, 1.0/60.0)
        return screenMan

    def on_stop(self):
        if os.path.isfile("qrcode.png"):
            os.remove("qrcode.png")


if __name__ == '__main__':
    AttendanceApp().run()
