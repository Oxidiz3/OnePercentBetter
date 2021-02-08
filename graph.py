from matplotlib import pyplot as plt
import numpy as np


def find_days_to_final_goal(start_value, end_value, iteration_amount):
    """
    Returns the total amount of days it will take to reach the goal calculated from the start_value, end_value, and
    iteration_amount.
    :param start_value: The starting value of the goal.
    :param end_value: The end value of the goal.
    :param iteration_amount: the percentage that represents the intensity of the goal in the form 0.1
    :return:
    """
    if start_value > end_value:
        iteration_amount = -1 * iteration_amount
    return int(np.ceil(np.log(end_value / start_value) / iteration_amount))


def graph_goal_progress(goal_name, iteration_amount, iteration_towards_goal, start_value, end_value, current_value):
    """
    Returns the name of the image created from the values input.
    :param goal_name: the name of the goal used to create the filename.
    :param iteration_amount: the percentage that the starting value will be increased by overtime.
    :param iteration_towards_goal: the days of progress the user has made.
    :param start_value: The value the user started there journey with.
    :param end_value: The value the user wants to achieve.
    :param current_value: The current value of the goal the user has done.
    :return: Returns the goal_name with the suffix .png, also saves an image with the same style.
    """
    total_days = find_days_to_final_goal(start_value, end_value, iteration_amount)
    goal_graph = np.linspace(start_value,end_value, total_days * 3)
    current_progress_graph = np.linspace(start_value, current_value, iteration_towards_goal * 3)
    ygoal_graph = start_value * np.exp(iteration_amount * goal_graph)
    ycurrent_progress_graph = start_value * np.exp(iteration_amount * current_progress_graph)
    plt.plot(goal_graph, ygoal_graph, color='black')
    plt.plot(current_progress_graph, ycurrent_progress_graph, color='red')
    plt.savefig(f'Images\{goal_name}.png')
    return f'{goal_name}.png'