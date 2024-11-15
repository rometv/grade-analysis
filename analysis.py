from datetime import datetime

import altair as alt
import pandas as pd
from altair import Chart
from tabulate import tabulate

from data_classes import Data
from dataframes import get_dataframes

root_dir = 'charts/'


def save(chart: Chart):
    time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    chart.save(fp=f'{root_dir}{chart.name}.html')


def table(df: pd.DataFrame):
    print(tabulate(df, headers='keys', tablefmt='fancy_grid'))


def analyse(data: Data):
    """
    Main function to analyse the data
    Parameters
    ----------
    data: Data object containing the data to be analysed, of type data_classes.Data.
    """
    student_df, submission_df, point_group_df = get_dataframes(data)

    # print(tabulate(student_df[:10], headers='keys', tablefmt='psql'))

    # testing(df=student_df)
    last_submission_date_by_grade(df=student_df)
    # general(student_df)
    # grade_change_by_submissions(student_df, submission_df, point_group_df)


def general(student_df: pd.DataFrame):
    table(student_df)
    chart = alt.Chart(student_df, name="general").mark_point().encode(
        x='grade:N',
        y='Last submission date'
    ).interactive()

    save(chart)


def grade_change_by_submissions(student_df: pd.DataFrame, submission_df: pd.DataFrame, point_group_df: pd.DataFrame):
    submission_data_sorted = submission_df.sort_values(by=['Student_ID', 'Submission_Time'])
    submission_data_sorted['Grade_Change'] = submission_data_sorted.groupby('Student_ID')['Submission_Grade'].diff()
    submission_data_sorted = submission_data_sorted.fillna(0)
    submission_data_sorted.loc[submission_data_sorted['Grade_Change'] < 0, 'Grade_Change'] = 0
    submission_data_sorted = submission_data_sorted[submission_data_sorted['Submission_Grade'] > 0]

    # submission_data_sorted = submission_data_sorted[submission_data_sorted['Submission_Time']].resample('H').mean()

    # print(submission_data_sorted[:30])
    chart = alt.Chart(submission_data_sorted[:1000], name="submissions").mark_point().encode(
        alt.Y('Submission_Grade:N', title='Submission Grade'),
        alt.X('Submission_Time:N', title='Submission Time'),
        size='Grade_Change:N',
        color='Student_ID'
    ).interactive().properties(width=500, height=500)
    save(chart)
    print(len(submission_data_sorted))
    table(submission_data_sorted)


def last_submission_date_by_grade(df: pd.DataFrame):
    # Filtering
    df = df[df['Time taken'] < 1500000]
    df = df[df['Last submission date'] != 0]
    df = df[df['Last submission date'] < datetime(2023, 11, 8)]
    q = df['Last submission date'].quantile(0.99)
    print("quantile", q)
    df = df[df['Last submission date'] <= q]
    df = df.infer_objects()
    df = df.reset_index()
    print(tabulate(df, headers='keys', tablefmt='psql'))
    # print(df.dtypes)
    scatter_plot = alt.Chart(df, name="general").mark_circle().encode(
        alt.Y('Max_Grade:N').bin(),
        alt.X('Last submission date').bin(),
        size='Submissions:N'
    ).interactive()

    save(scatter_plot)
