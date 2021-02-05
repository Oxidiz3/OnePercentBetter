from kivymd.app import MDApp
from kivymd.uix import MDAdaptiveWidget
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivy.core.window import Window


# FOR TESTING PURPOSES MAKES IT APROX THE SIZE OF A PHONE
Window.size = (300, 500)

KV = """
<TimedGoal>:
    MDRectangleFlatButton:
        text: root.text
        halign: "center"
        
Screen:
    MDBoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'One Percent Better'
            elevation: 8
            height: dp(40)
        
        MDLabel:
            text: "Goals"
            halign: "left"
            
        TimedGoal:
 
        MDBottomAppBar:
            MDFloatingActionButton:
                icon: "plus"
                elevation_normal:8
"""


class TimedGoal(MDRectangleFlatButton):
    text = "nothing special"


# class CountGoal(Widget):
#     goal_name = "goal_name"
#     goal_amount = "time"
#
#     def update(self, goal_name: str, goal_amount: str):
#         self.goal_name = goal_name
#         self.goal_amount = goal_amount


class UiApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "One Percent Better"
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.root = Builder.load_string(KV)

    def update(self):
        pass

    def create_goal(self):
        print("Create goal")


UiApp().run()