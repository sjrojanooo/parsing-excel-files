from pandas import DataFrame, read_excel

def read_combined_report(combined_report_path: str) -> DataFrame: 
    combined_report = read_excel(combined_report_path, converters={'Lot ID': str,'cooler_quantity': int})
    return combined_report

def transform_combine_columns(input_df: DataFrame) -> DataFrame: 
    output_df = input_df.rename(columns={'Lot ID': 'area',
                                                'Ranch':'report_date', 
                                                'Item Label': 'box_label', 
                                                'Item Name':'cooler_description', 
                                                'Quantity':'cooler_quantity'})\
                                .drop(columns=[input_df.columns[0]])
    return output_df

def aggregate_automated_report(input_df: DataFrame, report_date: str) -> DataFrame:
    input_df['report_date'] = report_date
    first = input_df.copy()
    first = input_df[input_df['area'].isin(['1'])]
    output_df = first.groupby(['report_date', 'cooler_description', 'box_label'], as_index=False).agg({'cooler_quantity':'sum'})
    return output_df    