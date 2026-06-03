import pandas as pd


def sort_df_by_date(df, ascending=False, column='Data'):
    """Sort df by 'column' with format '%d/%m/%Y'. ascending=False: end 1st."""

    col_to_datetime = lambda col: pd.to_datetime(col,format="%d/%m/%Y")
    return df.sort_values(by=column,
                          key=col_to_datetime,
                          ascending=ascending).reset_index(drop=True)