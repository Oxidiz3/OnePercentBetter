from database import Database

from kivymd.app import MDApp
from kivymd.uix.list import MDList, TwoLineIconListItem

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

data_base = Database()

# FOR TESTING PURPOSES MAKES IT APROX THE SIZE OF A PHONE
Window.size = (300, 500)

# TODO: Write Docstrings for every class


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
        list_of_goals = data_base.get_all_goals()
        for goal_dict in list_of_goals:
            self.ids.goal_list.add_widget(
                GoalListItem(
                    goal_name=goal_dict["goal_name"],
                    goal_amount=goal_dict["current_value"],
                    goal_icon=goal_dict["goal_icon"],
                )
            )


class GoalStatsScreen(Screen):
    pass


class GoalCreationScreen(Screen):
    end_goal_text = StringProperty("Select a goal type")
    start_goal_text = StringProperty("Select a goal type")
    goal_name = StringProperty("")
    icon = StringProperty("")

    start_value = NumericProperty(2)
    goal_intensity = NumericProperty(0.01)
    end_value = NumericProperty(0)
    iteration_towards_goal = NumericProperty(0)
    intensity = NumericProperty(0)

    def create_new_goal(self):
        data_base.create_goal(
            self.goal_name,
            self.icon,
            self.start_value,
            self.end_value,
            self.iteration_towards_goal,
            self.intensity,
        )

        print("create new goal")
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
    goal_name = StringProperty("goal_name")
    goal_icon = StringProperty("goal_icon")
    start_value = NumericProperty(0)
    end_value = NumericProperty(1234)
    iteration_percent = NumericProperty(0.1)
    iteration_towards_goal = NumericProperty(0)

    def __init__(self, goal_name, **kw):
        goal_dict = data_base.get_goal_from_name("goal_name")
        super().__init__(**kw)

    def get_goal_values(self):
        gd = self.goal_dict
        goal_name = gd["goal_name"]
        goal_icon = gd["goal_icon"]
        start_value = gd["start_value"]
        end_value = gd["start_value"]
        iteration_percent = gd["iteration_percent"]
        iteration_towards_goal = gd["iteration_towards_goal"]


class UiApp(MDApp):
    title = "1% Better"
    sm = ScreenManager()

    def build(self):
        # This is where you choose what screens you want to load
        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(GoalCreationScreen(name="goal_creation"))
        self.sm.add_widget(GoalStatsScreen(name="goal_stats"))
        return self.sm


UiApp().run()