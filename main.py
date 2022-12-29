import pandas as pd
from pandas import DataFrame
import os
import re
import importlib

constants = importlib.import_module('constants')

# locate the date reported anywhere on the page, in case of any format changes. 
def capture_report_date(updated_report_df: DataFrame):
    report_date = None
    for i in range(0, len(updated_report_df)): 
        for column in updated_report_df.columns: 
            value = str(updated_report_df.loc[i, column]).strip()
            if value != 'nan': 
                match_report_date = re.match(r'(\d{1,4}-\d{1,2}-\d{1,2})', value)
                if match_report_date: 
                    report_date = match_report_date.group(0)
                    break
    return report_date

# will capture commodity titles at each index level anywhere on the excel file. 
# return tuples/set of commodity and index
def identify_commodity_title_locations(updated_report_df: DataFrame, commodity_list: list):
    commodity_and_index_set = []; 
    for i in range(0, len(updated_report_df)):
        for column in updated_report_df.columns: 
            commodity = str(updated_report_df.loc[i, column]).strip()
            if commodity in commodity_list: 
                commodity_captured_set = (i, commodity) 
                commodity_and_index_set.append(commodity_captured_set) 
    return commodity_and_index_set

def main(): 
    updated_report_path = constants.updated_report_path
    commodity_list = constants.commodity_list

    updated_report = pd.read_excel(updated_report_path)
    report_date = capture_report_date(updated_report)
    commodity_index_list = identify_commodity_title_locations(updated_report, commodity_list)

    # make function
    product_df = DataFrame(commodity_index_list)
    test_list = []; 
    for i in range(0,len(product_df) -1):
        for x in range(int(product_df.loc[i, 0]), int(product_df.loc[i+1, 0])):
            test_list.append((x, str(product_df.loc[i, 1])))
            if x == product_df.loc[i+1, 0]:
                continue

    grouping_df = DataFrame(test_list)
    final_df = updated_report.join(grouping_df.set_index(0))
    final_df['report_date'] = report_date
    print(final_df)
if __name__ == '__main__':
    main()