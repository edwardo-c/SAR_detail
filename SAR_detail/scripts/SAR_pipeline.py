import pandas as pd


class SARPipeline():
    def __init__(self, sales_file_maps: dict, dimensions_file_map: dict):
        self.sales_file_maps = sales_file_maps
        self.dimensions_file_map = dimensions_file_map
        self.sales_dfs = {}
        self.qoutas_dfs = {}
    
    def load_sales(self):
            for map in self.sales_file_maps:
                 self.sales_dfs[map["alias"]] = pd.read_excel(map["file"], 
                                                              sheet_name=map["sheet_name"], 
                                                              header=map["row"]
                                                              )
    

    def load_dimensions(self):
        ...



    ...