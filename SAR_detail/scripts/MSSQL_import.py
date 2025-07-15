import pandas as pd
from sqlalchemy import create_engine, text

def import_into_mssql(df:pd.DataFrame, database:str, table:str, keep_schema:bool=True, if_exists:str='append'):
    '''
    Upload data to existing database table.
    Clears existing data and imports new data set
    '''

    ## match case on behaivor to append or overwrite
    engine = create_engine(database)

    # clear existing data without dropping schema
    if keep_schema:
        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM {table}"))

    # Push DataFrame to SQL table
    df.to_sql(table, con=engine, if_exists=if_exists, index=False)

    print(f"Data import succesfully into {table}")

