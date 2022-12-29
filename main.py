import pandas as pd
from pandas import DataFrame
import re
import importlib

constants = importlib.import_module('etl.constants')
report_transformations = importlib.import_module('etl.updated_report_transformations')

def main(): 

    updated_report_path = constants.updated_report_path
    commodity_list = constants.commodity_list
    updated_report = pd.read_excel(updated_report_path)
    report_date = report_transformations.capture_report_date(updated_report)
    commodity_index_list = report_transformations.identify_commodity_title_locations(updated_report, commodity_list)
    product_df = DataFrame(commodity_index_list)
    grouping_df = report_transformations.generate_index_dataframe(product_df)
    final_df = report_transformations.transform_final_df(updated_report, grouping_df, report_date) 
    final_df = report_transformations.filter_out_bad_values(final_df)
    final_df = report_transformations.rename_columns(final_df)
    report_transformations.write_out_clean_file(final_df)

if __name__ == '__main__':
    main()