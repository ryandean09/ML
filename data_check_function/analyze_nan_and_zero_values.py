import pandas as pd

def analyze_nan_and_zero_values(
    data, threshold, sort_column="零值+NAN佔比 (%)", ascending=False):
    """
    檢查0值和 nan 的數量，並檢查每個欄位的資料格式是否一致。
    
    參數:
    data: 資料來源，可以是CSV檔案的路徑或者Pandas DataFrame。
    threshold: 百分比閾值，例threshold=20，會回傳 零值+NAN佔比 (%) 大於20% 的欄位，當threshold=0會回傳全部。
    sort_column: 用來排序的欄位名稱，預設為"零值+NAN佔比 (%)"。
    ascending: 排序方式，預設為False(降序)。
    
    輸出:
    一個Pandas DataFrame，包含各欄位的零值與空白值統計、資料格式檢查結果。
    """

    if isinstance(data, str):
        file_source_pd = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        file_source_pd = data
    else:
        raise ValueError("輸入類型無效。輸入必須是檔案路徑或 Pandas DataFrame.")

    nan_values_per_column_in_range = file_source_pd.isnull().sum(axis=0)
    total_data_per_column = len(file_source_pd)
    nan_percentage_per_column = (nan_values_per_column_in_range / total_data_per_column) * 100
    zero_values_per_column_in_range = (file_source_pd == 0).sum(axis=0)
    zero_percentage_per_column = (zero_values_per_column_in_range / total_data_per_column) * 100
    total_zero_and_nan_per_column = (zero_values_per_column_in_range + nan_values_per_column_in_range)
    total_zero_and_nan_percentage_per_column = (total_zero_and_nan_per_column / total_data_per_column) * 100
    
    data_types = []
    for col in file_source_pd.columns:
        if file_source_pd[col].map(type).nunique() == 1:
            data_types.append(str(file_source_pd[col].map(type).iloc[0]).split("'")[1])
        else:
            data_types.append("different")

    values_df = pd.DataFrame(
        {
            "欄位名稱": nan_values_per_column_in_range.index,
            "零值+NAN佔比 (%)": total_zero_and_nan_percentage_per_column.values.round(
                2
            ),
            "空白值(NaN)數量": nan_values_per_column_in_range.values,
            "空白值(NaN)佔比 (%)": nan_percentage_per_column.values.round(2),
            "零值數量": zero_values_per_column_in_range.values,
            "零值佔比 (%)": zero_percentage_per_column.values.round(2),
            "資料格式檢查": data_types,
            "資料量": total_data_per_column,
        }
    )

    if threshold == 0:
        return values_df
    filtered_values_df = values_df[values_df["零值+NAN佔比 (%)"] > threshold]
    sorted_values_df = filtered_values_df.sort_values(by=sort_column, ascending=ascending)

    return sorted_values_df