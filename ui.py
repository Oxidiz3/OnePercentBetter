from typing import List

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, TwoLineIconListItem

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty, NumericProperty


l_goal_name: list[str] = ["Time Goal1", "Time Goal2", "Time Goal3", "Time Goal4"]
l_goal_icon: list[str] = ["counter", "alarm", "alarm", "alarm"]
l_goal_amount: list[int] = [100, 200, 300, 400]

# FOR TESTING PURPOSES MAKES IT APROX THE SIZE OF A PHONE
Window.size = (300, 500)


class Goal:
    def __init__(self):
        self.icon = ""
        self.intensity = 0
        self.goal_name = "goal_name"


class GoalListItem(TwoLineIconListItem):
    goal_name = StringProperty("goal_name")
    goal_amount = StringProperty("0")
    goal_icon = StringProperty("clock")

    def __init__(self, goal_name, goal_amount, goal_icon, **kwargs):
        self.goal_name = goal_name
        self.goal_amount = str(goal_amount)
        self.goal_icon = goal_icon
        super().__init__(**kwargs)


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.update_goals()

    def update_goals(self):
        for i in range(len(l_goal_name)):
            self.ids.goal_list.add_widget(
                GoalListItem(
                    goal_name=l_goal_name[i],
                    goal_amount=l_goal_amount[i],
                    goal_icon=l_goal_icon[i],
                )
            )

    pass


class GoalStatsScreen(Screen):
    pass


class GoalCreationScreen(Screen):
    end_goal_text = StringProperty("Text")

    def __init__(self, **kw):
        self.new_goal = Goal()
        super().__init__(**kw)

    def get_goal_type(self, type):
        print(type)
        self.new_goal.icon = type
        if type == "counter":
            self.end_goal_text = "What is your End Rep Goal"
        else:
            self.end_goal_text = "What is your End Time Goal"

    def get_intensity(self, intensity):
        print(intensity)
        self.new_goal.intensity = intensity

    def update_end_goal(self, label):
        self.ids.end_goal.text = label

    pass


class InfoScreen(Screen):
    pass


class UiApp(MDApp):
    title = "1% Better"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_goals(self):
        print("creating goals")
        pass

    def call_info(self):
        print("calling info")

    def build(self):
        # This is where you choose what screens you want to load
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(GoalCreationScreen(name="goal_creation"))
        # sm.add_widget(GoalStatsScreen(name="goal_stats"))
        return sm


UiApp().run()