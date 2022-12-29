import re
from pandas import DataFrame

# locate the date reported anywhere on the page, in case of any format changes. 
def capture_report_date(updated_report_df: DataFrame) -> str:
    report_date = None
    for i in range(0, len(updated_report_df)): 
        for column in updated_report_df.columns: 
            value = str(updated_report_df.loc[i, column]).strip()
            if value != 'nan': 
                # I use match here since the %Y-%m-%d format will always be at the beginning of the string. 
                match_report_date = re.search(r'(\d{1,4}-\d{1,2}-\d{1,2})', value)
                if match_report_date: 
                    report_date = match_report_date.group(0)
                    break
    return report_date

# will capture commodity titles at each index level anywhere on the excel file. 
# return tuples/set of commodity and index
def identify_commodity_title_locations(updated_report_df: DataFrame, commodity_list: list) -> DataFrame:
    commodity_and_index_set = []; 
    for i in range(0, len(updated_report_df)):
        for column in updated_report_df.columns: 
            commodity = str(updated_report_df.loc[i, column]).strip()
            if commodity in commodity_list: 
                commodity_captured_set = (i, commodity) 
                commodity_and_index_set.append(commodity_captured_set) 
    return DataFrame(commodity_and_index_set)

# capture indexes between next commodity
def generate_index_dataframe(product_df: DataFrame) -> DataFrame:
    test_list = []; 
    for i in range(0,len(product_df) -1):
        for x in range(int(product_df.loc[i, 0]), int(product_df.loc[i+1, 0]) -1):
            test_list.append((x, str(product_df.loc[i, 1])))
    grouping_df = DataFrame(test_list)
    return grouping_df

def transform_final_df(updated_report: DataFrame, grouping_df: DataFrame, report_date: str) -> DataFrame: 
    final_df = updated_report.join(grouping_df.set_index(0))
    final_df['report_date'] = report_date
    return final_df

def filter_out_bad_values(input_df: DataFrame) -> DataFrame: 
    output_df = input_df.dropna(subset=[input_df.columns[0], input_df.columns[1], input_df.columns[2]])
    output_df = output_df[[output_df.columns[0], output_df.columns[1],output_df.columns[7], output_df.columns[8]]]
    output_df = output_df[output_df[output_df.columns[0]].isin(['Commodities']) == False]
    output_df = output_df.loc[output_df[output_df.columns[0]].str[:5] != 'Total']
    return output_df 

def rename_columns(input_df: DataFrame) -> DataFrame:
    output_df = input_df.rename(columns={input_df.columns[0]:'description', 
                                        input_df.columns[1]: 'packed', 
                                        input_df.columns[2]: 'commodity'})
    output_df = output_df[['report_date', 'commodity', 'description', 'packed']]
    return output_df

def write_out_clean_file(input_df: DataFrame) -> None: 
    input_df.to_excel('./data/cleaned-report/clean-updated-counts.xlsx', index=False)
