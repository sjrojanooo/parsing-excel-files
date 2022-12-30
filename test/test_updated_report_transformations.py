import pytest
from pandas import DataFrame
from etl.updated_report import updated_report_transformations

def test_capture_report_date():
    input_df = DataFrame({'col1':['','','','','',''],
                          'col2':['','','','','',''],
                          'col3':['','','2022-12-12 11:24:23','','',''],
                          'col4':['','','','','',''],
    })
    report_date = updated_report_transformations.capture_report_date(input_df)
    assert report_date == '2022-12-12'