import pandas as pd
from sqlalchemy import create_engine

def load_into_mssql(df:pd.DataFrame, database:str, table:str, if_exists:str='replace'):
    '''
    Upload data to existing database table.
    Clears existing data and imports new data set
    '''
    engine = create_engine(database)

    df.to_sql(table, con=engine, if_exists=if_exists, index=False)

    print(f"Data import succesfully into {table}")

