from database import Database

from kivymd.app import MDApp
from kivymd.uix.list import TwoLineIconListItem, TwoLineAvatarIconListItem

from kivy.core.window import Window
from kivy.uix.screenmanager import (
    Screen,
    ScreenManager,
    SlideTransition,
    NoTransition,
)
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

data_base = Database()

# FOR TESTING PURPOSES MAKES IT APROX THE SIZE OF A PHONE
Window.size = (300, 500)

# TODO: Write Docstrings for every class


# class GoalListItem(TwoLineAvatarIconListItem):
#     goal_name = StringProperty("goal_name")
#     goal_amount = StringProperty("0")
#     goal_icon = StringProperty("clock")
#
#     def __init__(self, goal_name, goal_amount, goal_icon, **kwargs):
#         self.goal_name = goal_name
#         self.goal_amount = str(goal_amount)
#         self.goal_icon = goal_icon
#         super().__init__(**kwargs)


class GoalListItem(TwoLineAvatarIconListItem):
    # goal_name = StringProperty("goal_name")
    # goal_amount = StringProperty("0")
    # goal_icon = StringProperty("clock")

    def __init__(self, goal_name, goal_amount, goal_icon, **kwargs):
        self.goal_name = goal_name
        self.goal_amount = str(goal_amount)
        self.goal_icon = goal_icon
        super().__init__(**kwargs)


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_pre_enter(self, *args):
        self.update_goals()

    def update_goals(self):
        list_of_goals = data_base.get_all_goals()
        # Clear all widgets
        self.ids.goal_list.clear_widgets()
        # add all widgets to screen
        for goal_dict in list_of_goals:
            for i in range(1):
                self.ids.goal_list.add_widget(
                    GoalListItem(
                        goal_name=goal_dict["goal_name"],
                        goal_amount=goal_dict["current_value"],
                        goal_icon=goal_dict["goal_icon"],
                    )
                )


class GoalStatsScreen(Screen):
    goal_name = StringProperty("goal_name")
    goal_icon = StringProperty("alarm")
    start_value = NumericProperty(0)
    end_value = NumericProperty(1234)
    iteration_percent = NumericProperty(0.1)
    iteration_towards_goal = NumericProperty(0)
    goal_dict = {}

    def on_pre_enter(self, *args):
        print(self.goal_name)
        self.goal_dict = data_base.get_goal_from_name(self.goal_name)[0]
        print(self.goal_dict)
        self.get_goal_values()

    def get_goal_values(self):
        gd = self.goal_dict
        self.goal_name = gd["goal_name"]
        self.goal_icon = gd["goal_icon"]
        self.start_value = gd["start"]
        self.end_value = gd["end"]
        self.iteration_percent = gd["iteration_amount"]
        self.iteration_towards_goal = gd["iteration_goal"]

    def delete_goal(self):
        data_base.delete_goal(self.goal_name)


class GoalCreationScreen(Screen):
    end_goal_text = StringProperty("Select a goal type")
    start_goal_text = StringProperty("Select a goal type")
    goal_name = StringProperty("")
    icon = StringProperty("")

    start_value = ObjectProperty(2)
    end_value = ObjectProperty(0)
    goal_intensity = NumericProperty(0.01)
    iteration_towards_goal = NumericProperty(0)
    intensity = NumericProperty(0)

    def create_new_goal(self):
        create_try = data_base.create_goal(
            self.goal_name,
            self.icon,
            self.start_value,
            self.end_value,
            self.iteration_towards_goal,
            self.intensity,
        )
        if create_try:
            print("create new goal")
        else:
            print("goal failed")
        self.reset_goal()

    def reset_goal(self):
        # Reset Ui values
        self.ids.goal_name.text = ""
        self.ids.start_value.text = ""
        self.ids.end_value.text = ""
        self.start_goal_text = "Select a goal type"
        self.end_goal_text = "Select a goal type"

        # Reset values of variables
        self.goal_name = ""
        self.icon = ""
        self.start_value = 0
        self.end_value = 0
        self.iteration_towards_goal = 0
        self.intensity = 0.01


class InfoScreen(Screen):
    pass


class UIScreenManager(ScreenManager):
    current_goal_name = StringProperty()
    pass


class UiApp(MDApp):
    title = "1% Better"
    sm = ScreenManager(transition=NoTransition())

    def build(self):
        # This is where you choose what screens you want to load
        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(GoalCreationScreen(name="goal_creation"))
        self.sm.add_widget(GoalStatsScreen(name="goal_stats"))
        return self.sm

    def screen_change(self, screen_to_change_to: str, transition_direction="left"):
        self.sm.current = screen_to_change_to
        self.sm.transition.direction = transition_direction
        print("screen_change")

    def send_goal_name(self, goal_name):
        # Only works if goal stats screen is the 3 screen to be added
        self.sm.screens[2].goal_name = goal_name
        print(goal_name)
        print("tried 1")


app = UiApp()
app.run()