#
#
# def analyse(data: Data):
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_seq_item', None)
#     pd.set_option('display.multi_sparse', False)
#     pd.set_option('display.max_colwidth', None)
#     pd.set_option('display.max_colwidth', 50)
#     student_df, submission_df, point_group_df = get_dataframes(data)
#     # print(student_df[:5])
#
#     print(tabulate(student_df[:10], headers='keys', tablefmt='psql'))
#
#     testing(df=student_df)
#
#     # Initialise the dataframe
#     # df = pd.DataFrame(aio, columns=['id', 'time', 'grade', 'points'])
#     # df = df.loc[~(df == 0).all(axis=1)]
#     # df.dropna()
#
#     # Finding summaries.
#     # summary = df.groupby('id').agg({'grade': ['min', 'max', 'count', 'mean']})
#     # summary.columns = ['min_grade', 'max_grade', 'num_submissions', 'mean']
#     #
#     # # Getting some basic stats
#     # basic_stats(subs, users, summary, df, per_student)
#     #
#     # # Some plots
#     # avg_grade_to_submissions(student_df)
#     # max_grade_to_submissions(summary)
#     # plt.show()
#
# def basic_stats(subs, users, summary, df, student):
#     print(f'Total submissions: {subs}')
#     print(f'Graded (compiling) submissions: {df.shape[0]}')
#     print(f'Noncompilable submissions: {subs - df.shape[0]}')
#     print(f'Users: {users}')
#     print(f'Users with valid (compiling) solutions: {len(student)}')
#     print(f'Highest maximum grade: {max(summary["max_grade"]) * 100}%')
#     print(f'Highest number of submissions by user: {max(summary["num_submissions"])}')
#     print(f'Lowest number of submissions by user: {min(summary["num_submissions"])}')
#     # print(
#     #    f'Mean of submission grades excluding zero-grade submissions: '
#     #    f'{df[df["grade"] != 0].mean()["grade"] * 100 : .1f}%')
#     print(f'Mean of submission grades: {df["grade"].mean() * 100:.1f}%')
#     print(f'Mean of maximum (presumably last submission) grades: {summary["max_grade"].mean() * 100:.1f}%')
#     print(f'Mean of compiling submissions: {summary["num_submissions"].mean():.2f}')
#     print(f'Absolute mean of submissions: {subs / users: .1f}')
#
#
# def avg_grade_to_submissions(df):
#     """
#         Plots the average user grade to user submissions scatter plot. Color indicates the maximum grade.
#     :param df:
#     :return:
#     """
#     chart_subs_grade = alt.Chart(df, title="Number of submissions to maximum grade",
#                                  description="Plots the maximum grade to "
#                                              "number of submissions on "
#                                              "scatter plot.").mark_circle(
#
#     ).encode(
#         x='No_Of_Submissions',
#         y='Max_Grade',
#     ).interactive()
#
#     chart_subs_grade.save(f'submission_chart[{datetime.now().timestamp()}].html')
#
#     chart = alt.Chart(df, title="uh", description="uh").mark_circle().encode(x='No_Of_Submissions',
#                                                                              y='Max_Grade').interactive()
#     # chart.save(f'test_chart[{datetime.now().timestamp()}].html')
#
#     fig, ax = plt.subplots(1, figsize=(10, 12))
#     # plt.scatter(df['Max_Grade'], df['Max_Grade'], c=df['max_grade'], cmap='plasma')
#     # plt.colorbar(label='Max Grade')
#     # plt.xlabel('Number of Submissions')
#     # plt.ylabel('Average Grade')
#
#
# def max_grade_to_submissions(df):
#     """
#         Plots the maximum grade to number of submissions on scatter plot.
#     :param df:
#     :return:
#     """
#     # fig, ax = plt.subplots(1, figsize=(14, 7))
#     # plt.scatter(df['num_submissions'], df['max_grade'], c=np.random.rand(len(df)), alpha=0.7)
#     # plt.xlabel('Number of Submissions')
#     # plt.ylabel('Maximum Grade')
#
#
# def clustering(df):
#     df['ts'] = [datetime.timestamp(ts) for ts in df['time']]
#     X = df[['ts', 'grade']]
#     kmeans = KMeans(n_clusters=8)
#     kmeans.fit(X)
#
#     df['cluster'] = kmeans.labels_
#
#     return df

# def general(student_df: pd.DataFrame):
#     # table(student_df)
#     chart = alt.Chart(student_df, name="general").mark_point().encode(
#         x='grade:N',
#         y='Last submission date:T'
#     ).interactive()
#
#     save(chart)
#
# def grade_by_submissions(student_df: pd.DataFrame):
#     del student_df['Last submission date']
#     student_df = student_df[
#         (student_df['Submissions'] >= 0) &
#         (student_df['Submissions'] <= 50) &
#         (student_df['Max_Grade'] >= 0)
#         ]
#     print(student_df.head())
#     scatter = alt.Chart(student_df).mark_point(filled=True).encode(
#         alt.X('Submissions:Q', axis=alt.Axis(title='submissions')),
#         alt.Y('Max_Grade:Q', axis=alt.Axis(title='grade')),
#         tooltip=['Submissions', 'Time taken', 'Bad submissions']
#     )
#     trend_line = scatter.transform_regression(
#         'Submissions', 'Max_Grade', method='linear'
#     ).mark_line(color='red' )
#     new_chart = (scatter + trend_line).properties(title="Relationship between submissions and grades", width=500, height=500).interactive()
#     save(new_chart)
#
#
# def grade_change_by_submissions(student_df: pd.DataFrame, submission_df: pd.DataFrame, point_group_df: pd.DataFrame):
#     submission_data_sorted = submission_df.sort_values(by=['Student_ID', 'Submission_Time'])
#     submission_data_sorted['Grade_Change'] = submission_data_sorted.groupby('Student_ID')['Submission_Grade'].diff()
#     submission_data_sorted = submission_data_sorted.fillna(0)
#     submission_data_sorted.loc[submission_data_sorted['Grade_Change'] < 0, 'Grade_Change'] = 0
#     submission_data_sorted = submission_data_sorted[submission_data_sorted['Submission_Grade'] > 0]
#
#     # submission_data_sorted = submission_data_sorted[submission_data_sorted['Submission_Time']].resample('H').mean()
#
#     # print(submission_data_sorted[:30])
#     chart = alt.Chart(submission_data_sorted[:1000], name="submissions").mark_point().encode(
#         alt.Y('Submission_Grade:N', title='Submission Grade'),
#         alt.X('Submission_Time:N', title='Submission Time'),
#         size='Grade_Change:N',
#         color='Student_ID'
#     ).interactive().properties(width=500, height=500)
#     save(chart)
#     print(len(submission_data_sorted))
#     table(submission_data_sorted)
#
#
# def last_submission_date_by_grade(df: pd.DataFrame):
#     # Filtering
#     df = df[df['Time taken'] < 1500000]
#     df = df[df['Last submission date'] != 0]
#     df = df[df['Last submission date'] < datetime(2023, 11, 8)]
#     q = df['Last submission date'].quantile(0.99)
#     print("quantile", q)
#     df = df[df['Last submission date'] <= q]
#     df = df.infer_objects()
#     df = df.reset_index()
#     print(tab(df, headers='keys', tablefmt='psql'))
#     # print(df.dtypes)
#     scatter_plot = alt.Chart(df, name="general").mark_circle().encode(
#         alt.Y('Max_Grade:N').bin(),
#         alt.X('Last submission date').bin(),
#         size='Submissions:N'
#     ).interactive()
#
#     save(scatter_plot)

# def correlation_between_submissions_and_bad_grades(df: pd.DataFrame):
#     df = df.dropna()
#     df = df.drop('Last_submission_date', axis=1)
#
#     corr, _ = pearson(df['Max_Grade'], df['Bad_submissions'])
#     print('Pearsons correlation: %.3f' % corr)
#
#     print(df['Submissions'].sum())
#
#
#     chart = alt.Chart(df).mark_circle().encode(
#         y='Max_Grade',
#         x='Bad_submissions',
#     ).interactive()
#     #
#     #     chart_subs_grade = alt.Chart(df, title="Number of submissions to maximum grade",
#     #                                  description="Plots the maximum grade to "
#     #                                              "number of submissions on "
#     #                                              "scatter plot.").mark_circle(
#     #
#     #     ).encode(
#     #         x='No_Of_Submissions',
#     #         y='Max_Grade',
#     #     ).interactive()
#
#     chart.save('correlation_between_submissions_and_bad_grades.html')

# def average_time_between_submissions_to_bad_submissions(df: pd.DataFrame):
#     df = df.dropna()
#     df = df.drop('Last_submission_date', axis=1)
#
#     chart = alt.Chart(df).mark_circle().encode(
#         x="Bad_submissions",
#         y="Avg_time_between_submissions",
#     ).interactive()
#     corr, _ = pearson(df['Avg_time_between_submissions'], df['Bad_submissions'])
#
#     save(chart)


# def average_time_between_submissions_time_taken(df: pd.DataFrame):
#     df = df.dropna()
#     df = df.drop('Last_submission_date', axis=1)
#     chart = alt.Chart(df).mark_point().encode(
#         x='Avg_time_between_submissions',
#         y='Time_taken',
#         color='Max_Grade',
#         tooltip=['Submissions', 'Time_taken', 'Avg_time_between_submissions', 'Max_Grade']
#     ).properties(
#         title='Time Taken vs. Avg Time Between Submissions'
#     ).interactive()
#
#     corr, _ = pearson(df['Avg_time_between_submissions'], df['Time_taken'])
#     print('Pearsons correlation: %.3f' % corr)
#
#     save(chart)
#
#
# def average_time_between_submissions_and_grades(df: pd.DataFrame):
#     df = df.dropna()
#     df = df.drop('Last_submission_date', axis=1)
#     chart = (alt.Chart(df).mark_point().encode(
#         x='Max_Grade',
#         y='Avg_time_between_submissions',
#         size=alt.Size('Submissions'),
#     tooltip=['Submissions', 'Time_taken', 'Max_Grade'])
#              .properties(
#         title='Max Grade vs. Avg Time Between Submissions')
#              .interactive())
#
#     save(chart)