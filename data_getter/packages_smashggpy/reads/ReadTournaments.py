from data_getter.packages_smashggpy.util.ConnectorSQL import ConnectorSQL
from data_getter.packages_smashggpy.util.Logger import Logger
from data_getter.packages_smashggpy.common.Common import flatten, ifnull
import pandas as pd
import os
import pyodbc

from data_getter.packages_smashggpy.common.Constants import DATABASE, PWD, SERVER, UID, TABLE_DICTIONARY

def get_existing_tournament_urls():

    sql_connector = ConnectorSQL(server=SERVER,database=DATABASE,uid=UID, pwd=PWD)
    sql_connector.open_conn()
    tableResult = pd.read_sql("SELECT TournamentId, Name, URL FROM sgg.Tournament", sql_connector.conn)

    return tableResult.URL.to_list()