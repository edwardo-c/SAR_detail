from config.paths import SALES_PATH_2024, SALES_PATH_2025, DIMENSIONS_PATH
from scripts.SAR_pipeline import SARPipeline

if __name__ == "__main__":

    sales_file_map = (
        {"alias":"2025_direct", "file":SALES_PATH_2025, "sheet_name":"All Direct", "row":5},
        {"alias":"2025_pos", "file":SALES_PATH_2025, "sheet_name":"POS", "row":5},
        {"alias":"2024_direct", "file":SALES_PATH_2024, "sheet_name":"All Direct", "row":0},
        {"alias":"2024_pos", "file":SALES_PATH_2024, "sheet_name":"POS", "row":2},
    )

    dimensions_file_map = (
        {"alias": "users", "file": DIMENSIONS_PATH, "sheet_name":"pro_av", "row": 0},
        {"alias": "quotas", "file": DIMENSIONS_PATH, "sheet_name":"quotas", "row": 0},
        )

    pipeline = SARPipeline(sales_file_map, dimensions_file_map)
    pipeline.load_data()
    pipeline._process_data()
    pipeline.export_output()

    print("update complete!")