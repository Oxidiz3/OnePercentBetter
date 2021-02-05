import sqlite3
from sqlite3 import Error


class Database:
    def create_table(self, create_table_sql) -> bool:
        """ creates a table given a Connection object and a sql statement.
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            return True
        except Error as e:
            print(e)
            return False

    def __init__(self, db_file=r'Database/onepercent.db'):
        """ Initializes the database for the app, it will handle all of the setup required for getting the database running
            and started.
            :param db_file: a string to the database path.
        """

        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def close_connection(self):
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    carl = Database()
    sql_create_goals_table = """ CREATE TABLE IF NOT EXISTS goals (
                                            id integer PRIMARY KEY,
                                            start integer NOT NULL,
                                            end integer NOT NULL
                                            );
                                     """
    carl.close_connection()
