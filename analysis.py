import sys
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def analyse(subs, users, per_student, aio):
    # Initialise the dataframe
    df = pd.DataFrame(aio, columns=['id', 'time', 'grade'])
    df = df.loc[~(df == 0).all(axis=1)]
    df.dropna()

    # Finding summaries..
    summary = df.groupby('id').agg({'grade': ['min', 'max', 'count', 'mean']})
    summary.columns = ['min_grade', 'max_grade', 'num_submissions', 'mean']

    # Getting some basic stats
    basic_stats(subs, users, summary, df, per_student)

    # Clustering
    # df = clustering(df)

    # Some plots
    avg_grade_to_submissions(summary)
    max_grade_to_submissions(summary)
    plt.show()

    # Exit
    exit_message = "Program end."
    sys.exit(f"EXIT: {exit_message}")


def basic_stats(subs, users, summary, df, student):
    print(f'Total submissions: {subs}')
    print(f'Graded (compiling) submissions: {df.shape[0]}')
    print(f'Noncompilable submissions: {subs - df.shape[0]}')
    print(f'Users: {users}')
    print(f'Users with valid (compiling) solutions: {len(student)}')
    print(f'Highest minimum grade: {max(summary["min_grade"]) * 100}%')
    print(f'Highest maximum grade: {max(summary["max_grade"]) * 100}%')
    print(f'Highest number of submissions by user: {max(summary["num_submissions"])}')
    print(f'Lowest number of submissions by user: {min(summary["num_submissions"])}')
    print(
        f'Mean of submission grades excluding zero-grade submissions: {round(df[df["grade"] != 0].mean()["grade"], 2) * 100}%')
    print(f'Mean of submission grades: {round(df["grade"].mean(), 2) * 100}%')
    print(f'Mean of maximum (presumably last submission) grades: {round(summary["max_grade"].mean(), 2) * 100}%')
    print(f'Mean of compiling submissions: {round(summary["num_submissions"].mean(), 1)}')
    print(f'Absolute mean of submissions: {round(subs / users, 1)}')


def clustering(df):
    df['ts'] = [datetime.timestamp(ts) for ts in df['time']]
    X = df[['ts', 'grade']]

    kmeans = KMeans(n_clusters=8)
    kmeans.fit(X)

    df['cluster'] = kmeans.labels_

    return df


def avg_grade_to_submissions(df):
    """
        Plots the average user grade to user submissions scatter plot. Color indicates the maximum grade.
    :param df:
    :return:
    """
    fig, ax = plt.subplots(1, figsize=(10, 12))
    plt.scatter(df['num_submissions'], df['mean'], c=df['max_grade'], cmap='plasma')
    plt.colorbar(label='Max Grade')
    plt.xlabel('Number of Submissions')
    plt.ylabel('Average Grade')


def max_grade_to_submissions(df):
    """
        Plots the maximum grade to number of submissions scatter plot.
    :param df:
    :return:
    """
    fig, ax = plt.subplots(1, figsize=(14, 7))
    plt.scatter(df['num_submissions'], df['max_grade'], c=np.random.rand(len(df)), alpha=0.7)
    plt.xlabel('Number of Submissions')
    plt.ylabel('Maximum Grade')
