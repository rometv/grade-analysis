dataframes = {
    "submission_df": None,
    "point_group_df": None,
    "current_zip_name": None,
    "start_date": None,
    "end_date": None,
}

def load_data(submission_df, point_group_df, zip_name):
    dataframes["submission_df"] = submission_df
    dataframes["point_group_df"] = point_group_df
    dataframes["current_zip_name"] = zip_name
    dataframes["start_date"] = submission_df["timestamp"].min()
    dataframes["end_date"] = submission_df["timestamp"].max()

def get(name):
    return dataframes.get(name)