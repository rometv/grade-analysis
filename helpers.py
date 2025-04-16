import pandas as pd
from flask import request

from data_store import get_df


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    submissions = get_df(
        'submission_df'
    )

    start_date = submissions['Submission_Time'].min()
    end_date = submissions['Submission_Time'].max()

    filtered_df = df

    start_date_filter = request.args.get("start_date", start_date.strftime('%d/%m/%Y'))
    end_date_filter = request.args.get("end_date", end_date.strftime('%d/%m/%Y'))

    if start_date_filter is not None and end_date_filter is not None:
        start_date_filter = pd.to_datetime(start_date_filter, format='%d/%m/%Y').strftime('%Y-%m-%d')
        end_date_filter = pd.to_datetime(end_date_filter, format='%d/%m/%Y').strftime('%Y-%m-%d')

        start_date_filter = pd.to_datetime(start_date_filter, format='%Y-%m-%d')
        end_date_filter = pd.to_datetime(end_date_filter, format='%Y-%m-%d')

        if start_date_filter and end_date_filter and start_date_filter < end_date_filter:
            if start_date_filter >= start_date and end_date_filter <= end_date:
                filtered_df = filtered_df.drop(df[df['Submission_Time'] <= start_date_filter].index)
                filtered_df = filtered_df.drop(df[df['Submission_Time'] >= end_date_filter].index)

    return filtered_df
