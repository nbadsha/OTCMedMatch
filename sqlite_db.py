import sqlite3
from sqlite3 import Error
import pandas as pd
from med_info import Medicine

class MedDB(object):

    def __init__(self):
        # os.chdir(r'C:\Users\DollaR\OneDrive\Documents\Final Year Project\app')
        database = r"medicine.db"        
        self.conn = self.create_connection(database)



    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn




    def findOneMed(self, med_name):
        """
        Query tasks by priority
        :param conn: the Connection object
        :param priority:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM med_info WHERE med_name LIKE '{}'".format(med_name))

        rows = cur.fetchall()
        return rows

    def run_insert(self, data):
        med_name = data.med_name
        med_des = data.med_des
        med_use = data.med_use
        med_sideffect = data.med_sideffect
        med_info = Medicine(med_name, med_des, med_use, med_sideffect)
        c = self.conn.cusor()
        c.execute(med_info.insert())
        self.conn.commit()

    def insert_batch(self, dataFrame):
        dataFrame.apply(lambda data: self.run_insert(data), axis=1)
        








"""CREATE TABLE "med_info" (
	"id"	INTEGER NOT NULL,
	"med_name"	TEXT NOT NULL,
	"med_des"	TEXT NOT NULL,
	"med_use"	TEXT NOT NULL,
	"med_sideffect"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)"""

