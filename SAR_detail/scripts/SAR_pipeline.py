import os
import shutil
import tempfile
from pathlib import Path
import pandas as pd
from config.paths import CSV_EXPORT_PATH, TEMP_CSV

class SARPipeline():
    def __init__(self, file_map: set):
        self.file_map = file_map
        self.dfs = {}
        self.output_data = pd.DataFrame()
        self.temp_dir = tempfile.mkdtemp()  # temporary local cache
    
    def _process_data(self):
        self.add_pay_structure_to_pos()
        self._apply_rename_map()
        self.output_data = self._concat_output_data()
        self.output_data = self._join_users()
        self._fill_missing_part_numbers()
        self._split_credit_date()
        self._add_rep_role_key()
        self.cleanup_temp_dir()

    def _process_reclass(self):

        def consolidate():
            pos_cols = {
                    "Credit": "credit",
                    "Reclass" : "reclass",
                    "Reclass $": "amount",
                    "Reclass Cat": "product_category",
                    "Customer": "distributor",
                    "SoldToName": "customer_name",
                    "PiiPartNumber": "part_number",
                    "SAR Month": "credit_month"
                }

            direct_cols ={
                    "Credit": "credit",
                    "Reclass": "reclass",
                    "Reclass $": "amount",
                    "Reclass Cat": "product_category",
                    "Account": "acct_num",
                    "Customer Name": "customer_name",
                    "Inventory CD": "part_number",
                    "SAR Month": "credit_month",
                }

            # rename columns            
            self.dfs["reclass_pos"] = self.dfs["reclass_pos"].rename(columns=pos_cols)
            self.dfs["reclass_direct"] = self.dfs["reclass_direct"].rename(columns=direct_cols)

            # return only renamed columns
            self.dfs["reclass_pos"] = self.dfs["reclass_pos"][list(pos_cols.values())]
            self.dfs["reclass_direct"] = self.dfs["reclass_direct"][list(direct_cols.values())]

            # concatenate to single reclass data frame
            self.dfs["reclass"] = pd.concat([self.dfs["reclass_pos"], self.dfs["reclass_direct"]])

        def unpivot():
            df = self.dfs["reclass"]
            self.dfs["reclass"] = pd.melt(
                df,
                id_vars=[col for col in df.columns if col not in {"credit", "reclass"}],
                value_vars=["credit", "reclass"],
                var_name="credit_type",
                value_name="rep"
                )

        def process_amount():
            self.dfs["reclass"]["amount"] = self.dfs["reclass"].apply(
                lambda row: 
                    row["amount"] * -1 
                    if row["credit_type"] == "credit" 
                    else row["amount"],
                    axis=1)

        def overwrite_credit_type():
            self.dfs["reclass"]["credit_type"] = "reclass"

        def convert_months():
            month_map = {
                "January": 1,
                "February": 2,
                "March": 3,
                "April": 4,
                "May": 5,
                "June": 6,
                "July": 7,
                "August": 8,
                "September": 9,
                "October": 10,
                "November": 11,
                "December": 12
            }

            self.dfs["reclass"]["credit_month"].replace(
                month_map, inplace= True
            )

        def add_year():
            self.dfs["reclass"]["credit_year"] = 2025

        consolidate()
        unpivot()
        process_amount()
        overwrite_credit_type()
        convert_months()
        add_year()

        # correct part number, if null part, input category: Can be completed with "output data"

    def load_data(self):
        '''
        Copies Excel files to a local temp folder and reads from there for faster loading.
        '''
        start_time = pd.Timestamp.now()

        # Copy files to local temp folder
        local_file_map = []
        for entry in self.file_map:
            src_path = entry["file"]
            local_path = Path(self.temp_dir) / Path(src_path).name
            shutil.copy2(src_path, local_path)
            # Update path to local copy
            new_entry = entry.copy()
            new_entry["file"] = str(local_path)
            local_file_map.append(new_entry)

        # Load files from local paths
        self.dfs = {
            entry['alias']: pd.read_excel(
                entry["file"],
                sheet_name=entry["sheet_name"],
                header=entry["row"]
            )
            for entry in local_file_map
        }

        elapsed = (pd.Timestamp.now() - start_time).total_seconds()
        print(f"Loaded files in {elapsed:.2f} seconds from local cache")
        
    def add_pay_structure_to_pos(self):
        val = "pos"
        self.dfs["2025_pos"]["pay_structure"] = val
        self.dfs["2024_pos"]["pay_structure"] = val
    
    def _apply_rename_map(self):
        rename_map = {
            "2025_direct": {
                "Credit": "rep",
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
                "Credit": "rep",
                "pay_structure": "pay_structure",
                "Customer": "distributor",
                "SoldToName": "customer_name",
                "PiiPartNumber": "part_number",
                "PiiCategory": "product_category",
                "ShipQuantity": "qty",
                "ExtendedSales": "amount",
                "PeriodDate": "credit_date",
            },
            "2024_direct": {
                "2025 Credit": "rep",
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
                "2025 Credit": "rep",
                "Customer": "distributor",
                "SoldToName": "customer_name",
                "PiiPartNumber": "part_number",
                "PiiCategory": "product_category",
                "ShipQuantity": "qty",
                "ExtendedSales": "amount",
                "PeriodDate": "credit_date",
                "pay_structure": "pay_structure",
            },
        }

        # Rename and subset in one loop
        for alias, col_map in rename_map.items():
            self.dfs[alias] = self.dfs[alias].rename(columns=col_map)
            self.dfs[alias] = self.dfs[alias][list(col_map.values())]


    def _concat_output_data(self):
        return pd.concat(
            [
                df 
                for alias, df in self.dfs.items() 
                if alias not in {"users", "quotas"}
            ], 
                ignore_index=True
            )

    def _join_users(self):
        users = self.dfs["users"]["Full Name"].unique()
        return self.output_data[self.output_data["rep"].isin(users)]

    def _fill_missing_part_numbers(self):
        self.output_data["part_number"] = self.output_data["part_number"].fillna(
            self.output_data["product_category"]
        )

    def _split_credit_date(self):
        self.output_data["credit_date"] = pd.to_datetime(self.output_data["credit_date"], errors="coerce")

        self.output_data["credit_month"] = self.output_data["credit_month"].fillna(self.output_data["credit_date"].dt.month)
        self.output_data["credit_year"] = self.output_data["credit_year"].fillna(self.output_data["credit_date"].dt.year)
        
    def _add_rep_role_key(self):
        self.output_data["rep_role_key"] = (
            self.output_data["rep"].astype(str) + "|" + self.output_data["product_category"]
            )
    
    def export_output(self, path=CSV_EXPORT_PATH):
        self.output_data.to_csv(path, index=False)

    def cleanup_temp_dir(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)