from SAR_detail.scripts.SAR_pipeline import SARPipeline
import pandas as pd

def test_add_month_year():
    date_col = 'date'
    my_data = {
        date_col: [
            '2025-07-01',
            '2025-08-02',
            '2025-04-25',
        ]
    }
    my_df = pd.DataFrame(my_data)

    my_df = SARPipeline._add_month_year(my_df, date_col, year='credit_year', month='credit_month')

    assert 'credit_year' in my_df.columns
    assert 'credit_month' in my_df.columns
    assert list(my_df['credit_year']) == [2025, 2025, 2025]
    assert list(my_df['credit_month']) == [7, 8, 4]
