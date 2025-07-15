import pandas as pd
from config.paths import QUOTAS, DATABASE
from scripts.MSSQL_import import import_into_mssql

df = pd.read_csv(QUOTAS)
import_into_mssql(df, DATABASE, "pro_av_quotas_2025")