import os
from pandas import DataFrame, read_excel

from etl.updated_report import updated_report_transformations, constants
from etl.automated_report import automated_report_transformations

def main(): 
    
    # report file paths
    base_path = './data'
    commodity_list = constants.commodity_list
    updated_report_path = os.path.join(base_path, 'updated-cooler-counts/weekly-validation.xlsx')
    combined_report_path = os.path.join(base_path, 'automated-cooler-totals/combined-report.xlsx')
    box_labels_path = os.path.join(base_path, 'box-labels/box_labels.xlsx')

    # updated production counts
    updated_report = read_excel(updated_report_path)
    report_date = updated_report_transformations.capture_report_date(updated_report)
    product_df = updated_report_transformations.identify_commodity_title_locations(updated_report, commodity_list)
    grouping_df = updated_report_transformations.generate_index_dataframe(product_df)
    final_updated_report = updated_report_transformations.combine_titles_to_products(updated_report, grouping_df, report_date) 
    final_updated_report = updated_report_transformations.filter_out_bad_values(final_updated_report)
    final_updated_report = updated_report_transformations.rename_columns(final_updated_report)
    updated_report_transformations.write_out_file(final_updated_report, './data/cleaned-report/clean-updated-counts.xlsx')

    # box labels for description mapping
    box_labels = updated_report_transformations.read_box_labels(box_labels_path)
    final_updated_report = final_updated_report.merge(box_labels, on=['description'], how='left')

    # automated report aggregation
    combined_report = automated_report_transformations.read_combined_report(combined_report_path)
    combined_report = automated_report_transformations.transform_combine_columns(combined_report)
    combined_report = automated_report_transformations.aggregate_automated_report(combined_report, report_date)
    
    # generate final validated report
    combine_updated_with_automated_report = updated_report_transformations.combined_reports(final_updated_report, combined_report)
    final_validation_report = updated_report_transformations.transform_combined_df(combine_updated_with_automated_report)
    updated_report_transformations.write_out_file(final_validation_report, './data/final-validated-report/final-validated-report.xlsx')

if __name__ == '__main__':
    main()