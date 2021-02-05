from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.core.window import Window

# FOR TESTING PURPOSES MAKES IT APROX THE SIZE OF A PHONE
Window.size = (300, 500)

KV = """
Screen:
    BoxLayout
        orientation: 'vertical'
        MDToolbar:
            title: 'One Percent Better'
            elevation: 8
            height: dp(40)
            
        MDBottomAppBar:
            MDToolbar:
                icon: 'plus-circle'
                
"""


class MainApp(MDApp):
    def build(self):
        screen = Builder.load_string(KV)
        return screen


MainApp().run()