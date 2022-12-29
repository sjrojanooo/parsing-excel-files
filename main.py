from pandas import DataFrame, read_excel

from etl import updated_report_transformations, constants

def main(): 

    updated_report_path = constants.updated_report_path
    commodity_list = constants.commodity_list
    updated_report = read_excel(updated_report_path)
    report_date = updated_report_transformations.capture_report_date(updated_report)
    product_df = updated_report_transformations.identify_commodity_title_locations(updated_report, commodity_list)
    grouping_df = updated_report_transformations.generate_index_dataframe(product_df)
    final_df = updated_report_transformations.transform_final_df(updated_report, grouping_df, report_date) 
    final_df = updated_report_transformations.filter_out_bad_values(final_df)
    final_df = updated_report_transformations.rename_columns(final_df)
    updated_report_transformations.write_out_clean_file(final_df)

if __name__ == '__main__':
    main()