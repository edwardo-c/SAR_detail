# used for one time loads into the schema

import pandas as pd
from config.paths import QUOTAS, DATABASE
from SAR_detail.scripts.load import load_into_mssql


df = pd.read_csv(QUOTAS)
load_into_mssql(df, DATABASE, "pro_av_quotas_2025")

