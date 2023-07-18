import pyodbc
from data_getter.packages_smashggpy.util.Logger import Logger


class ConnectorSQL(object):
    def __init__(self, server, database, uid, pwd):
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.server = server
        self.database = database
        self.uid = uid
        self.pwd = pwd
        self.conn = None
        self.cursor = None

    def open_conn(self):
        self.conn = pyodbc.connect(
            driver = self.driver,
            server = self.server,
            database= self.database,
            uid = self.uid,
            pwd = self.pwd
        )
        self.cursor = self.conn.cursor()
        self.cursor.fast_executemany=True
        # Logger.debug('Opened connection to {}/{}'.format(self.server, self.database))

    def commit(self):
        self.cursor.commit()

    def fetchall(self):
        self.cursor.fetchall()

    def execute(self, base_query, variables):
        self.cursor.executemany(base_query, variables)

    def close_conn(self):
        self.cursor.close()
        self.conn.close()
        # Logger.debug('Closed connection to {}/'.format(self.server, self.database))
