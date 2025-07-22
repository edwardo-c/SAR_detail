from config.paths import SALES_PATH_2024, SALES_PATH_2025, DIMENSIONS_PATH, DATABASE, RECLASS
from scripts.load import load_into_mssql
from scripts.SAR_pipeline import SARPipeline

if __name__ == "__main__":

    print("loading...")

    file_map = (
        {"alias":"2025_direct", "file": SALES_PATH_2025, "sheet_name":"All Direct", "row": 5},
        {"alias":"2025_pos", "file": SALES_PATH_2025, "sheet_name":"POS", "row": 5},
        {"alias": "reclass_pos", "file": RECLASS, "sheet_name": "reclass_pos", "row": 0},
        {"alias": "reclass_direct", "file": RECLASS, "sheet_name": "reclass_non_pos", "row": 0},
        {"alias": "2024_direct", "file": SALES_PATH_2024, "sheet_name": "All Direct", "row": 0},
        {"alias": "2024_pos", "file": SALES_PATH_2024, "sheet_name": "POS", "row": 2},
        {"alias": "users", "file": DIMENSIONS_PATH, "sheet_name":"pro_av", "row": 0},
        {"alias": "quotas", "file": DIMENSIONS_PATH, "sheet_name":"quotas", "row": 0},
        )

    pipeline = SARPipeline(file_map)
    pipeline.load_data()
    pipeline._process_reclass()
    pipeline._process_data()
    pipeline.export_output()

    print("complete")

    # table = 'sales'
    # load_into_mssql(pipeline.output_data, DATABASE, table)

    # print(f"load into {table} table complete")