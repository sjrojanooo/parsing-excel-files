import re
from pandas import DataFrame, read_excel

# constants
# commodity list 
commodity_list = ['Cauliflower', 'Cauliflower Organic', 'Wrap', 'Wrap Organic','Naked Flat Pack Lettuce',
       'Romaine Hearts','Romaine Hearts Organic','Romaine Flat Pack','Romaine Flat Pack Organic',
       'Romaine Cellos','Mix Leaf','Mix Leaf Organic','Mix Leaf Cellos','Broccoli','Broccoli Organic',
       'Mix Vegetables Rates','Broccoli Bulk Organic']

# locate the date reported anywhere on the page, in case of any format changes. 
def capture_report_date(updated_report_df: DataFrame) -> str:
    report_date = None
    for i in range(0, len(updated_report_df)): 
        for column in updated_report_df.columns: 
            value = str(updated_report_df.loc[i, column]).strip()
            if value != 'nan': 
                # I use match here since the %Y-%m-%d format will always be at the beginning of the string. 
                match_report_date = re.match(r'(\d{1,4}-\d{1,2}-\d{1,2})', value)
                if match_report_date: 
                    report_date = match_report_date.group(0)
                    break
    return report_date

# will capture commodity titles at each index level anywhere on the excel file. 
# return tuples/set of commodity and index
def identify_commodity_title_locations(updated_report_df: DataFrame, commodity_list: list) -> DataFrame:
    commodity_and_index_set = []; 
    max_row = len(updated_report_df) - 1 
    for i in range(0, len(updated_report_df)):
        for column in updated_report_df.columns: 
            commodity = str(updated_report_df.loc[i, column]).strip()
            if commodity in commodity_list: 
                commodity_captured_set = (i, commodity) 
                commodity_and_index_set.append(commodity_captured_set)
        if i == max_row: 
            commodity = commodity_and_index_set[-1][1]
            commodity_and_index_set.append((i, commodity))
    return DataFrame(commodity_and_index_set)

# capture indexes between next commodity
def generate_index_dataframe(product_df: DataFrame) -> DataFrame:
    test_list = []; 
    for i in range(0,len(product_df) - 1):
        for x in range(int(product_df.loc[i, 0]), int(product_df.loc[i+1, 0]) - 1):
            test_list.append((x, str(product_df.loc[i, 1])))
    grouping_df = DataFrame(test_list)
    return grouping_df

# join indexed_title dataframe to product names in each section. 
def combine_titles_to_products(updated_report: DataFrame, grouping_df: DataFrame, report_date: str) -> DataFrame: 
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

def write_out_file(input_df: DataFrame, path: str) -> None: 
    input_df.to_excel(path, index=False)


def read_box_labels(box_labels_path: str) -> DataFrame: 
    output_df = read_excel(box_labels_path)[['box_label', 'description']]
    return output_df    


def combined_reports(updated_report_df: DataFrame, automated_report_df: DataFrame) -> DataFrame:
    final_validation_report = updated_report_df.merge(automated_report_df, on=['report_date','box_label'], how='left')
    return final_validation_report

def transform_combined_df(final_df: DataFrame) -> DataFrame:
    output_df = final_df.copy()
    output_df = output_df[['report_date', 'commodity', 'description', 
                                                        'cooler_description', 'box_label','packed', 'cooler_quantity']]
    output_df['difference'] = output_df['cooler_quantity'] - output_df['packed']
    return output_df
