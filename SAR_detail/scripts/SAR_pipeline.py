import pandas as pd


class SARPipeline():
    def __init__(self, sales_file_map: set, dimensions_file_map: set):
        self.sales_file_map = sales_file_map
        self.dimensions_file_map = dimensions_file_map
        self.sales_dfs = {}
        self.dimensions_dfs = {}
    
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


    def transform_sales(self):
        '''
        
        '''
        ...