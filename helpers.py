import pandas as pd
from flask import request

from data_store import get


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """ Filters a dataframe based on request arguments."""
    filtered_df = df
    submissions = get('submission_df')

    start_date = submissions['timestamp'].min()
    end_date = submissions['timestamp'].max()

    timezone = start_date.tz

    start_date_filter = request.args.get("start_date", start_date.strftime('%d/%m/%Y'))
    end_date_filter = request.args.get("end_date", end_date.strftime('%d/%m/%Y'))

    start_date_filter = pd.to_datetime(start_date_filter, format='%d/%m/%Y')
    end_date_filter = pd.to_datetime(end_date_filter, format='%d/%m/%Y')

    start_date_filter = start_date_filter.tz_localize(timezone)
    end_date_filter = end_date_filter.tz_localize(timezone)

    if start_date_filter and end_date_filter and start_date_filter <= end_date_filter:
        if start_date_filter.date() >= start_date.date() and end_date_filter.date() <= end_date.date():
            filtered_df = filtered_df[
                (filtered_df['timestamp'].dt.date >= start_date_filter.date()) &
                (filtered_df['timestamp'].dt.date <= end_date_filter.date())
                ].copy()

    return filtered_df
