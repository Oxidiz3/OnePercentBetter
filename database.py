import logging
import math
import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self, db_file=r"Database/onepercent.db"):
        """Initializes the database for the app, it will handle all of the setup required for getting the database
        running and started.
        :param db_file: a string to the database path.
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(
                db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            sql_create_goals_table = """ CREATE TABLE IF NOT EXISTS goals (
                                                        id integer PRIMARY KEY,
                                                        name text NOT NULL,
                                                        goal_icon text NOT NULL,
                                                        start integer NOT NULL,
                                                        end integer NOT NULL,
                                                        iteration_amount float NOT NULL,
                                                        iteration_to_goal int NOT NULL
                                                        );
                                                 """
            self.cur = self.conn.cursor()
            self.cur.execute(sql_create_goals_table)
            logging.info(sqlite3.version)
            #self.create_goal("Lose Weight", "alarm", 10, 100, 5, .25)
            #self.create_goal("Learn to Program", "alarm", 1, 100, 1, .13)
            #self.create_goal("Sleep More", "alarm", 4, 8, 3, .03)
        except Error as e:
            logging.info(e)

    def create_goal(
        self,
        goal_name,
        goal_icon,
        start_value,
        end_value,
        iteration_towards_goal,
        iteration_percent,
    ):
        """
        Creates a goal
        :param goal_name: name of the goal
        :param goal_icon: icon needed for the goal
        :param start_value: starting amount
        :param end_value: ending value
        :param iteration_towards_goal: how close to the goal are you.
        :param iteration_percent: the percentage the iteration goes up by.
        :return: returns true if the transaction occurred false if an error was encountered.
        """
        # Checking to make sure there are no duplicate entries in the database already.
        select_sql = """SELECT name, goal_icon, start, end, iteration_amount, iteration_to_goal FROM goals 
                        WHERE name = ? AND goal_icon = ?;"""
        dataTuple = (goal_name, goal_icon)
        self.cur.execute(select_sql, dataTuple)
        goalList = self.cur.fetchall()
        # If there are no duplicate entries then the database goes ahead with the transaction.
        if not goalList and len(goal_name) != 0:
            if start_value > end_value:
                iteration_percent *= -1
            dataTuple = (
                goal_name,
                goal_icon,
                start_value,
                end_value,
                iteration_percent,
                iteration_towards_goal,
            )
            sql = """ INSERT INTO goals(name,goal_icon, start,end, iteration_amount, iteration_to_goal)
                      VALUES(?,?,?,?,?,?); """
            self.cur.execute(sql, dataTuple)
            self.conn.commit()
            return True
        else:
            return False

    def delete_goal(self, name):
        delete_sql = f"""DELETE from goals where name = '{name}';"""
        try:
            r_set = self.conn.execute(delete_sql)
        except Error as e:
            error = str(e.__dict__["orig"])
            print(error)
        else:
            print(f"No of records deleted : {r_set.rowcount}")
            self.conn.commit()

    def get_all_goals(self):
        """
        Grabs all the goals in the database and returns them as a list...hopefully.
        :return:
        """

        sql = """ SELECT name, goal_icon, start, end, iteration_amount, iteration_to_goal FROM goals"""
        self.cur.execute(sql)
        goalList = self.cur.fetchall()
        tmpList = list()
        for i in goalList:
            tmp = dict()
            tmp["goal_name"] = i[0]
            tmp["goal_icon"] = i[1]
            tmp["start"] = i[2]
            tmp["end"] = i[3]
            tmp["iteration_amount"] = i[4]
            tmp["iteration_goal"] = i[5]
            tmp["current_value"] = int(i[2] * math.exp(i[4] * i[5]))
            tmpList.append(tmp)
        return tmpList

    def get_goal_from_name(self, name):
        """
        Grabs all the goals in the database and returns them as a list...hopefully.
        :return:
        """

        sql = f" SELECT name, goal_icon, start, end, iteration_amount, iteration_to_goal FROM goals WHERE name = '{name}'"
        self.cur.execute(sql)
        goalList = self.cur.fetchall()
        tmpList = list()
        if not goalList:
            print('Name was not in database.')
            return False
        for i in goalList:
            tmp = dict()
            tmp["goal_name"] = i[0]
            tmp["goal_icon"] = i[1]
            tmp["start"] = i[2]
            tmp["end"] = i[3]
            tmp["iteration_amount"] = i[4]
            tmp["iteration_goal"] = i[5]
            tmp["current_value"] = int(i[2] * math.exp(i[4] * i[5]))
            tmpList.append(tmp)
        return tmpList

    def update_increment_towards_goal(self, name):
        """
        Updates a records increment_towards_goal to the passed value.
        :param name: the name used to get the item.
        :param increment_towards_goal: the new value for increment_towards_goal.
        :return:
        """
        select_sql = f"SELECT increment_towards_goal FROM goals WHERE name = '{name}'"
        self.cur.execute(select_sql)
        lis = self.cur.fetchall()
        increment_towards_goal = lis[0]
        print(increment_towards_goal)
        sql = f"UPDATE goals SET increment_towards_goal = {increment_towards_goal} WHERE name = '{name}'"
        self.cur.execute(sql)
        print(self.get_all_goals())
'''
if __name__ == "__main__":
    data = Database()
    print(data.get_all_goals())
    #data.delete_goal('Lose Weight')
    #data.delete_goal('Learn to Program')
    #data.delete_goal('Sleep More')
'''