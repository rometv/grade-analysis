dataframes = {
    "student_df": None,
    "submission_df": None,
    "point_group_df": None,
    "last_point_groups_df": None,
    "current_zip_name": None
}

def load_data(student_df, submission_df, point_group_df, last_df, zip_name):
    print("Loading data...")
    dataframes["student_df"] = student_df
    dataframes["submission_df"] = submission_df
    dataframes["point_group_df"] = point_group_df
    dataframes["last_point_groups_df"] = last_df
    dataframes["current_zip_name"] = zip_name

def get_df(name):
    return dataframes.get(name)