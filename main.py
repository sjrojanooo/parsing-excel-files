import pandas as pd
import os
import re
import importlib

constants = importlib.import_module('constants')

# locate the date reported anywhere on the page, in case of any format changes. 
def capture_report_date(updated_report_df):
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

def find_titles(): 
    pass

def main(): 
    updated_report_file_path = constants.updated_report_path
    updated_report = pd.read_excel(updated_report_file_path)
    report_date = capture_report_date(updated_report)
    print(report_date)
    for i in range(0, len(updated_report)):
        for column in updated_report.columns: 
            value = str(updated_report.loc[i, column]).strip()
            print(value)

if __name__ == '__main__':
    main()