from data_getter.packages_smashggpy.util.ConnectorSQL import ConnectorSQL
from data_getter.packages_smashggpy.util.Logger import Logger
from data_getter.packages_smashggpy.common.Common import flatten, ifnull
import pandas as pd
import os
import pyodbc

from data_getter.packages_smashggpy.common.Constants import DATABASE, PWD, SERVER, UID, TABLE_DICTIONARY

def insert_records(l: list, TABLE_NAME, overwrite_mode=False):
    
    if len(l) == 0:
        Logger.info('No record could be insert for: {}'.format(TABLE_NAME))
        return None
    viable_entry_list = []
    sql_connector = ConnectorSQL(server=SERVER,database=DATABASE,uid=UID, pwd=PWD)
    sql_connector.open_conn()

    main_df = pd.DataFrame.from_records([s.__dict__ for s in l]).drop_duplicates()
    try:
        if overwrite_mode:
            id_list = []
            for i in main_df.id.tolist():
                id_list.append([i])
            sql_connector.execute(TABLE_DICTIONARY[TABLE_NAME]["OW"], id_list)
        
        sql_connector.execute(TABLE_DICTIONARY[TABLE_NAME]["INS"], main_df.values.tolist())
        viable_entry_list = main_df.id.to_list()
    except pyodbc.IntegrityError as ex:
        print(ex)
        if ex.args[0] == '23000':
            Logger.debug('Problem entering record into database.')

    sql_connector.commit()
    sql_connector.close_conn()
    Logger.info(f'{len(viable_entry_list)} rows inserted to the {TABLE_NAME} table')

    return viable_entry_list