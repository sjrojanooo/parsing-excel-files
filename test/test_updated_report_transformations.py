import pytest
from pandas import DataFrame
from etl.updated_report import updated_report_transformations

def test_capture_report_date():
    input_df = DataFrame({'col1':['','','','','',''],
                          'col2':['','','','','',''],
                          'col3':['','','2022-12-12 11:24:23','','',''],
                          'col4':['','','','','','']})
    report_date = updated_report_transformations.capture_report_date(input_df)
    assert report_date == '2022-12-12'

def test_capture_commodity_titles():
    input_df = DataFrame({'col1':['','','Cauliflower','','','', 'Broccoli','','']})
    commodity_list = updated_report_transformations.commodity_list
    output_df = updated_report_transformations.identify_commodity_title_locations(input_df, commodity_list)
    assert output_df.loc[0,output_df.columns[1]] == 'Cauliflower'
    assert output_df.loc[0, output_df.columns[0]] == 2
    assert output_df.loc[1,output_df.columns[1]] == 'Broccoli'
    assert output_df.loc[1, output_df.columns[0]] == 6

def test_generate_index_dataframe():
    input_df = DataFrame({'col1':['','','Cauliflower','','','', 'Broccoli','','']})
    commodity_list = updated_report_transformations.commodity_list
    titles_captured_df = updated_report_transformations.identify_commodity_title_locations(input_df, commodity_list)
    output_df = updated_report_transformations.generate_index_dataframe(titles_captured_df)
    assert len(output_df) == 4

def test_filter_out_bad_values(): 
    input_df = DataFrame({'col1':['valid', None , 'Commodities', 'Total Broccoli', None, None],
                         'col2':['valid', 'invalid', 'invalid', 'invalid', 'invalid','invalid'],
                         'col3':['valid', 'invalid', 'invalid', 'invalid', 'invalid','invalid'],
                         'col4':['valid', 'invalid', 'invalid', 'invalid', 'invalid','invalid'],
                         'col5':['valid', 'invalid', 'invalid', 'invalid', 'invalid','invalid'],
                         'col6':['valid', 'invalid', 'invalid', 'invalid', 'invalid','invalid'],
                         'col7':['valid', 'invalid', 'invalid', 'invalid', 'invalid','invalid'],
                         'col8':['valid', 'invalid', 'invalid', 'invalid', 'invalid','invalid'],
                         'col9':['valid', 'invalid', 'invalid', 'invalid', 'invalid','invalid']})

    output_df = updated_report_transformations.filter_out_bad_values(input_df)
    assert len(output_df) == 1

def test_rename_columns(): 
    input_df = DataFrame({'col1':[''],
                          'col2':[''],
                          'col3':[''],
                          'report_date':['']})

    output_df = updated_report_transformations.rename_columns(input_df)
    assert output_df.columns.values.tolist() == ['report_date', 'commodity', 'description', 'packed']