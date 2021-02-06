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


class Goal(TwoLineIconListItem):
    goal_name = StringProperty("goal_name")
    goal_amount = StringProperty("0")
    goal_icon = StringProperty("clock")

    def __init__(self, goal_name, goal_amount, goal_icon, **kwargs):
        self.goal_name = goal_name
        self.goal_amount = str(goal_amount)
        self.goal_icon = goal_icon
        super().__init__(**kwargs)


class MainScreen(Screen):
    pass


class GoalStatsScreen(Screen):
    pass


class GoalCreationScreen(Screen):
    pass


class InfoScreen(Screen):
    pass


class UiApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "One Percent Better"
        super().__init__(**kwargs)

    # def on_start(self):
    #     for i in range(len(l_goal_name)):
    #         self.root.main.ids.goal_list.add_widget(
    #             Goal(
    #                 goal_name=l_goal_name[i],
    #                 goal_amount=l_goal_amount[i],
    #                 goal_icon=l_goal_icon[i],
    #             )
    #         )

    def create_goals(self):
        print("creating goals")
        pass

    def call_info(self):
        print("calling info")

    def build(self):
        sm = ScreenManager()
        # sm.add_widget(MainScreen(name="main"))
        sm.add_widget(GoalCreationScreen(name="goal_creation"))
        # sm.add_widget(GoalStatsScreen(name="goal_stats"))
        return sm


UiApp().run()