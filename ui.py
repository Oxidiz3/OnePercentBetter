from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

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


class GoalListItem(TwoLineAvatarIconListItem):
    # goal_name = StringProperty("goal_name")
    # goal_amount = StringProperty("0")
    # goal_icon = StringProperty("clock")

    def __init__(self, goal_name, goal_amount, goal_icon, **kwargs):
        self.goal_name = goal_name
        self.goal_amount = str(goal_amount)
        self.goal_icon = goal_icon
        super().__init__(**kwargs)


class GoalDialogBox(MDDialog):
    dialog_text = StringProperty()


class MainScreen(Screen):
    """"""

    def on_pre_enter(self, *args):
        """Called before the Main screen is opened"""
        self.update_goals()

    def update_goals(self):
        """Get's all goals and updates what they should look like

        :return:
        """
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
    """Screen where all of the goal stats are dispalyed"""

    goal_name = StringProperty("goal_name")
    goal_icon = StringProperty("alarm")
    start_value = NumericProperty(0)
    current_value = NumericProperty(10)
    end_value = NumericProperty(1234)
    iteration_percent = NumericProperty(0.1)
    iteration_towards_goal = NumericProperty(0)
    goal_dict = {}

    def on_pre_enter(self, *args):
        """Called before the Main screen is opened"""
        print(self.goal_name)
        self.goal_dict = data_base.get_goal_from_name(self.goal_name)[0]
        print(self.goal_dict)
        self.get_goal_values()

    def get_goal_values(self):
        """Calls to the database and gets goal values"""
        gd = self.goal_dict
        self.goal_name = gd["goal_name"]
        self.goal_icon = gd["goal_icon"]
        self.start_value = gd["start"]
        self.current_value = gd["current_value"]
        self.end_value = gd["end"]
        self.iteration_percent = gd["iteration_amount"]
        self.iteration_towards_goal = gd["iteration_goal"]

    def delete_goal(self):
        """Delete goal from database"""
        data_base.delete_goal(self.goal_name)


class GoalCreationScreen(Screen):
    """Screen where we create goals"""

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
        """Creates goals in database"""
        create_try = data_base.create_goal(
            self.goal_name,
            self.icon,
            self.start_value,
            self.end_value,
            int(self.iteration_towards_goal),
            self.intensity,
        )
        if create_try:
            print("create new goal")
        else:
            print("goal failed")
        self.reset_goal()

    def reset_goal(self):
        """Resets goal pages so that it looks fresh"""
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
    """Where we display info about our app"""

    pass


class UiApp(MDApp):
    """Where all main logic is stored"""

    title = "1% Better"
    sm = ScreenManager(transition=NoTransition())
    dialog = None
    current_goal_name = ""

    def build(self):
        """builds all scenes
        :return: screen manager
        """
        # This is where you choose what screens you want to load
        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(GoalCreationScreen(name="goal_creation"))
        self.sm.add_widget(GoalStatsScreen(name="goal_stats"))
        self.sm.add_widget(InfoScreen(name="info"))
        return self.sm

    def screen_change(self, screen_to_change_to: str, transition_direction="left"):
        """
        :param screen_to_change_to: Name of screen we want to chang to
        :param transition_direction: Which way we transiton
        """
        self.sm.current = screen_to_change_to
        self.sm.transition.direction = transition_direction
        print("screen_change")

    def send_goal_name(self, goal_name):
        """
        :param goal_name: send goal name to stats screen
        """
        # Only works if goal stats screen is the 3 screen to be added
        self.sm.screens[2].goal_name = goal_name
        print(goal_name)
        print("tried 1")

    def refresh_main_screen(self):
        """ calls update screen on main screen """
        self.sm.screens[0].update_goals()
        print("main is refreshed")

    def show_dialog_box(self, goal_name, *args):
        """
            Displays dialog box when you click on left icon of goal
        :param goal_name: name of goal to display
        :param args: REQUIRED FOR KIVY
        """
        goal_dict = data_base.get_goal_from_name(goal_name)[0]
        self.current_goal_name = goal_name
        if not self.dialog:
            self.dialog = GoalDialogBox(
                title=goal_name,
                text="You've completed this goal "
                + str(goal_dict["iteration_goal"])
                + " times so far",
                # size_hint=(0.75, 1),
                buttons=[
                    # ON_RELEASE CANNOT EQUAL A FUNCTION... LEAVE THE PARENTHESES OFF
                    MDFlatButton(text="Cancel", on_release=self.close_dialog_box),
                    MDRaisedButton(text="Log goal", on_release=self.increment_goal),
                ],
            )
        self.dialog.open()

    def increment_goal(self, *args):
        """increment goals + 1
        :param args: REQUIRED FOR KIVY
        """
        goal_dict = data_base.get_goal_from_name(self.current_goal_name)[0]
        goal_dict["iteration_goal"] += 1
        data_base.delete_goal(self.current_goal_name)

        gd = goal_dict
        data_base.create_goal(
            gd["goal_name"],
            gd["goal_icon"],
            gd["start"],
            gd["end"],
            gd["iteration_goal"],
            gd["iteration_amount"],
        )
        self.increment_goal()
        self.refresh_main_screen()
        self.close_dialog_box()

    def close_dialog_box(self, *args):
        """Closes dialog box after it's been opened
        :param args: REQUIRED FOR KIVY
        """
        self.dialog.dismiss()


app = UiApp()
app.run()