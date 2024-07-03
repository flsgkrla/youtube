from project_data_load import load_data, preprocess_data, process_outliers, process_data

def check_change():
    df_cleaned, df_replaced, df_pivot = process_data()
    col_list = ['totalMinutes', 'videoDays', 'videoLikeCnt', 'videoCommentCnt', 'videoViewCnt']

    changed_values = []

    for col in col_list:
        diff_rows = df_cleaned.loc[df_cleaned[col] != df_replaced[col]]

        for idx, row in diff_rows.iterrows():
            original_value = row[col]
            replaced_value = df_replaced.at[idx, col]  # .at[]: 해당 idx, col 값 가져옴
            diff = replaced_value - original_value
            changed_values.append({
                'index': idx,
                'column': col,
                'original_value': original_value,
                'replaced_value': replaced_value,
                'difference': diff
            })

    for change in changed_values:
        print(f"Index {change['index']} - Column {change['column']}: original={change['original_value']}, replaced={change['replaced_value']}, diff={change['difference']}")

check_change()


##

