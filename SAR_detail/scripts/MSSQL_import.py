from config.paths import CSV_EXPORT_PATH, DATABASE
import pandas as pd
from sqlalchemy import create_engine, text

# 1. Load CSV into DataFrame
df = pd.read_csv(CSV_EXPORT_PATH)

# Optional: Clean/rename columns
# df.columns = ['id', 'sale_date', 'amount', 'product_name']

# 2. Connect to SQL Server
engine = create_engine(DATABASE)

# 3. clear existing data without dropping schema
with engine.connect() as conn:
    conn.execute(text("DELETE FROM sales"))

# 4. Push DataFrame to SQL table
df.to_sql('sales', con=engine, if_exists='append', index=False)

print("✅ Data imported successfully.")

