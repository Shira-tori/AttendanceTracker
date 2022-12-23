from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.graphics import Color
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivymd.uix.tab import MDTabsBase
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivymd.theming import ThemableBehavior
from kivy.uix.image import Image
from kivymd.uix.list import ILeftBody, OneLineAvatarListItem
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Canvas, Ellipse
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.filechooser import FileChooser
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivy.app import App
from kivy.properties import StringProperty
import os
#rom kivy.utils import get_application_path
#rom kivy.resources import user_data_dir
# from kivy_garden.filebrowser import FileBrowser
#rom plyer import Filechooser



class Content(MDBoxLayout):
	manager = ObjectProperty()
	nav_drawer = ObjectProperty()

class Navigator(MDNavigationDrawer):
	pass


class AvatarSampleWidget(ILeftBody, Image):
	pass

class DrawerList(ThemableBehavior, MDList):
	pass

class BaseShadowMDCard(MDCard, RectangularElevationBehavior):
    pass

class NavLayout(MDNavigationLayout):
    screen_man = ObjectProperty()
    content = ObjectProperty()

    def update(self, dt):
        if self.screen_man.current == "Home":
            self.content.settings_list.disabled = False
            self.content.profile_list.disabled = False
            self.content.home_list.disabled = True

        elif self.screen_man.current == "Settings":
            self.content.settings_list.disabled = True
            self.content.home_list.disabled = False
            self.content.profile_list.disabled = False
        
        elif self.screen_man.current == "Profile":
            self.content.profile_list.disabled = True
            self.content.settings_list.disabled = False
            self.content.home_list.disabled = False
            


class Tab(FloatLayout, MDTabsBase):
    pass

class MainScreen(MDScreen):
    profpage = ObjectProperty()

class ScreenMan(ScreenManager):
    pass

class TEACHERSACC(MDApp):
    image_source = StringProperty('')  # this will hold the path of the selected image
    file_chooser = FileChooser()

    def build(self):

        self.image_source = ""
        self.file_chooser = FileChooser()
        self.file_chooser.filters = ['*.jpg', '*.png']  # allow the user to select only image files
        self.file_chooser.bind(on_selection=self.file_selected)

        # Try to get the root directory of the internal storage on Android
        root_dir = os.path.expanduser('~/storage/emulated/0')
        if os.path.exists(root_dir):
            file_chooser.path = root_dir
        else:
            # On iOS, the root directory of the internal storage is '/private/var/mobile/Containers/Data/Application'
            root_dir = '/private/var/mobile/Containers/Data/Application'
            if os.path.exists(root_dir):
                self.file_chooser.path = root_dir

        mainScreen = MainScreen()   
        navlayout = NavLayout()
        screenMan = ScreenMan()
        mainScreen.nav_layout.screen_man.current = "Home"
        Clock.schedule_interval(mainScreen.nav_layout.update, 1.0/60.0)
        # self.image = Image(source='')
        # mainScreen.add_widget(self.image)
        return mainScreen

    



    def file_selected(self, selection):
        if len(selection) > 0:  # make sure a file was actually selected
            image_path = selection[0]
            # now you can use the image_path to display the image in your application
            # for example, you can use an AsyncImage widget to load the image asynchronously:
            self.ids.userimage.source = image_path
            self.add_widget(self.userimage)


        


if __name__ == '__main__':
    TEACHERSACC().run()

