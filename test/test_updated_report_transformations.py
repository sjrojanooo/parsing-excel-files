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
    assert len(output_df) == 4

