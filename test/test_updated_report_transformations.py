from turtle import update
import pytest
from pandas import DataFrame
from etl.updated_report import updated_report_transformations, constants

def test_capture_report_date():
    input_df = DataFrame({'col1':['','','','','',''],
                          'col2':['','','','','',''],
                          'col3':['','','2022-12-12 11:24:23','','',''],
                          'col4':['','','','','','']})
    report_date = updated_report_transformations.capture_report_date(input_df)
    assert report_date == '2022-12-12'

def test_capture_commodity_titles():
    input_df = DataFrame({'col1':['','','Cauliflower','','','', 'Broccoli','','']})
    output_df = updated_report_transformations.identify_commodity_title_locations(input_df, constants.commodity_list)
    assert output_df.loc[0,output_df.columns[1]] == 'Cauliflower'
    assert output_df.loc[0, output_df.columns[0]] == 2
    assert output_df.loc[1,output_df.columns[1]] == 'Broccoli'
    assert output_df.loc[1, output_df.columns[0]] == 6

def test_generate_index_dataframe():
    input_df = DataFrame({'col1':['','','Cauliflower','','','', 'Broccoli','','']})
    titles_captured_df = updated_report_transformations.identify_commodity_title_locations(input_df, constants.commodity_list)
    output_df = updated_report_transformations.generate_index_dataframe(titles_captured_df)
    print(output_df)
    assert len(output_df) == 4

# def transform_final_df(updated_report: DataFrame, grouping_df: DataFrame, report_date: str) -> DataFrame: 
#     final_df = updated_report.join(grouping_df.set_index(0))
#     final_df['report_date'] = report_date
#     return final_df

# def filter_out_bad_values(input_df: DataFrame) -> DataFrame: 
#     output_df = input_df.dropna(subset=[input_df.columns[0], input_df.columns[1], input_df.columns[2]])
#     output_df = output_df[[output_df.columns[0], output_df.columns[1],output_df.columns[7], output_df.columns[8]]]
#     output_df = output_df[output_df[output_df.columns[0]].isin(['Commodities']) == False]
#     output_df = output_df.loc[output_df[output_df.columns[0]].str[:5] != 'Total']
#     return output_df 

# def rename_columns(input_df: DataFrame) -> DataFrame:
#     output_df = input_df.rename(columns={input_df.columns[0]:'description', 
#                                         input_df.columns[1]: 'packed', 
#                                         input_df.columns[2]: 'commodity'})
#     output_df = output_df[['report_date', 'commodity', 'description', 'packed']]
#     return output_df

# def write_out_file(input_df: DataFrame, path: str) -> None: 
#     input_df.to_excel(path, index=False)


# def read_box_labels(box_labels_path: str) -> DataFrame: 
#     output_df = read_excel(box_labels_path)[['box_label', 'description']]
#     return output_df    


# def combined_reports(updated_report_df: DataFrame, automated_report_df: DataFrame) -> DataFrame:
#     final_validation_report = updated_report_df.merge(automated_report_df, on=['report_date','box_label'], how='left')
#     return final_validation_report

# def transform_combined_df(final_df: DataFrame) -> DataFrame:
#     output_df = final_df.copy()
#     output_df = output_df[['report_date', 'commodity', 'description', 
#                                                         'cooler_description', 'box_label','packed', 'cooler_quantity']]
#     output_df['difference'] = output_df['cooler_quantity'] - output_df['packed']
#     return output_df
