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
