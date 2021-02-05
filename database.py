import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ Connects the database to the program and returns a Connection object.
        :param db_file: Path to the database file.
        :return: Connection Object or none.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ creates a table given a Connection object and a sql statement.
    :param conn: Connection Object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        return True
    except Error as e:
        print(e)
        return False


def init(databasePath):
    """ Initializes the database for the app, it will handle all of the setup required for getting the database running
        and started.

        :param databasePath: a string to the database path.
    """
    sql_create_goals_table = """ CREATE TABLE IF NOT EXISTS goals (
                                    id integer PRIMARY KEY,
                                    start integer NOT NULL,
                                    end integer NOT NULL
                                    );
                             """
    conn = create_connection(databasePath)

    if conn is not None:
        create_table(conn, sql_create_goals_table)
    else:
        print("Error! cannot create the database connection.")
    if conn:
        conn.close()


if __name__ == '__main__':
    init(r"Database/onepercent.db")

