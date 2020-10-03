import sqlite3
import pathlib
from sqlite3 import Error

class DatabaseUtility() : 
    def initialize(self):
        path = pathlib.Path().absolute()
        database = r"{path}/messagespy.db".format(path=path)

        sql_create_conversations_table = """ CREATE TABLE IF NOT EXISTS conversations (
                                        id integer PRIMARY KEY,
                                        chat_id text NOT NULL,
                                        conversation_type text NOT NULL,
                                        name text NOT NULL
                                    ); """

        # create a database connection
        conn = self.create_connection(database)

        # create tables
        if conn is not None:
            # create projects table
            self.create_table(conn, sql_create_conversations_table)

        return conn
        
        
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def get_conversation_name(self, id):
        conn = self.initialize()
        try:
            cur = conn.cursor()
            cur.execute("SELECT name FROM conversations WHERE chat_id=?", (str(id),))

            convTuple = cur.fetchone()
            if convTuple != None:
                return convTuple[0]
        except Error as e:
            print(e)
        finally:
            if (conn):
                conn.close()
            print("The SQLite connection is closed")

        return None
    def get_conversation(self, name, conversation_type):
        conn = self.initialize()
        conv = {}
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM conversations WHERE name=? and conversation_type=?", (str(name),conversation_type))

            convTuple = cur.fetchone()
            if convTuple != None:
                conv = dict([('chat_id',convTuple[1]), ('name',convTuple[3]), ('conversation_type',convTuple[2])])
        except Error as e:
            print(e)
        finally:
            if (conn):
                conn.close()
            print("The SQLite connection is closed")

        return conv

    def create_conversation(self, chat_id, name, conversation_type):
        conn = self.initialize()
        conv = {}
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM conversations WHERE chat_id=? and conversation_type=?", (str(chat_id),conversation_type))

            convTuple = cur.fetchone()
            cur.close()

            if convTuple == None:
                convals = [str(chat_id), conversation_type, str(name)]
                cur = conn.cursor()
                cur.execute("INSERT INTO conversations(chat_id, conversation_type, name) VALUES(?,?,?)", convals)
                conn.commit()
                conv = dict([('chat_id',str(chat_id)), ('name',name), ('conversation_type',conversation_type)])
                cur.close()
        except Error as e:
            print(e)
        finally:
            if (conn):
                conn.close()
            print("The SQLite connection is closed")

        return conv
