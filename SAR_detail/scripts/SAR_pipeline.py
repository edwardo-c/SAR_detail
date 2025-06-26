import pandas as pd
from config.paths import CSV_EXPORT_PATH

POS_COLUMNS = [
    "credit",
    "reclass",
    "distributor",
    "customer_name",
    "part_number",
    "product_category",
    "qty",
    "amount",
    "credit_date",
    ]

class SARPipeline():
    def __init__(self, sales_file_map: set, dimensions_file_map: set):
        self.sales_file_map = sales_file_map
        self.dimensions_file_map = dimensions_file_map
        self.sales_dfs = {}
        self.dimensions_dfs = {}
        self.output_data = pd.DataFrame()
    
    @staticmethod
    def read_file_map(file_map):
        '''
        returns: dict of {alias : dataframe}
        '''
        return {
            entry['alias']: 
            pd.read_excel(
                entry["file"], 
                sheet_name=entry["sheet_name"], 
                header=entry["row"]
                )
                for entry in file_map
            }

    def load_data(self):
        self.sales_dfs = self.read_file_map(self.sales_file_map)
        self.dimensions_dfs = self.read_file_map(self.dimensions_file_map)

    def _transform_pos_data():
        ...
    
    def parse_alias(alias):
        year, source = alias.split("_", 1)
        return year, source

    @staticmethod
    def _rename_map() -> dict:
        return {
            "2025_direct": {
                "Credit": "credit",
                "Reclass" : "reclass", 
                "Account" : "acct_num", 
                "Customer Name": "customer_name", 
                "Type": "pay_structure", 
                "Inventory CD": "part_number", 
                "Qty": "qty",  
                "Amount": "amount", 
                "Classification(Sales Category)": "product_category", 
                "Invoice Date": "credit_date",
                },
            "2025_pos": {
                "Credit": "credit",
                "Reclass": "reclass",
                "Customer": "distributor",
                "SoldToName": "customer_name",
                "PiiPartNumber": "part_number",
                "PiiCategory": "product_category",
                "ShipQuantity": "qty",
                "ExtendedSales": "amount",
                "PeriodDate": "credit_date",
                },
            "2024_direct": {
                "2025 Credit": "credit",
                "Customer Account Number": "acct_num",
                "Customer Name": "customer_name",
                "2025 SAR Rule": "pay_structure",
                "Inventory CD": "part_number",
                "Qty": "qty",
                "Amount": "amount",
                "Classification(Sales Category)": "product_category",
                "Invoice Date": "credit_date",
            },
            "2024_pos": {
                "2025 Rep": "credit",
                "Customer": "distributor",
                "SoldToName": "customer_name",
                "PiiPartNumber": "part_number",
                "PiiCategory": "product_category",
                "ShipQuantity": "qty",
                "ExtendedSales": "amount",
                "PeriodDate": "credit_date"
            },
        }

    @staticmethod
    def rename_columns(df: pd.DataFrame, rename_map: dict):
        '''
        Returns: truncated dataframe with only renamed_to columns
        '''
        return df.rename(columns=rename_map)[rename_map.values()]

    def _concat_output_data(self):
        return pd.concat(self.sales_dfs.values(), ignore_index=True)

    def _unpivot_pro_av(self):
        return pd.melt(
            self.output_data,
            id_vars=[col for col in self.output_data.columns if col not in {"credit", "reclass"}],
            value_vars=["credit", "reclass"],
            var_name="credit_type",
            value_name="rep"
        )

    def _join_users(self):
        users = self.dimensions_dfs["users"]["Full Name"].unique()
        return self.output_data[self.output_data["rep"].isin(users)]

    def _fill_missing_part_numbers(self):
        self.output_data["part_number"] = self.output_data["part_number"].fillna(
            self.output_data["product_category"]
        )

    def _split_credit_date(self):
        self.output_data["credit_date"] = pd.to_datetime(self.output_data["credit_date"], errors="coerce")

        self.output_data["credit_month"] = self.output_data["credit_date"].dt.month
        self.output_data["credit_year"] = self.output_data["credit_date"].dt.year
    
    def export_output(self, path=CSV_EXPORT_PATH):
        self.output_data.to_csv(path, index=False)

    def _process_data(self):
        rename_map = self._rename_map()

        for alias, df in self.sales_dfs.items():
            df = self.rename_columns(df, rename_map[alias])
            self.sales_dfs[alias] = df

        self.output_data = self._concat_output_data()
        self.output_data = self._unpivot_pro_av()
        self.output_data = self._join_users()
        self._fill_missing_part_numbers()
        self._split_credit_date()