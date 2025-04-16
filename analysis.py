import altair as alt
import pandas as pd

from helpers import filter_dataframe
from data_store import get_df


# alt.data_transformers.disable_max_rows() # Max rows error b like

def general_data() -> [str, str, any]:
    students = get_df('student_df')
    submissions = get_df('submission_df')

    start_date = submissions['Submission_Time'].min()
    end_date = submissions['Submission_Time'].max()

    general = [
        ('student_count', 'Tudengeid kokku', students.shape[0]),
        ('submissions_count', 'Esitusi kokku', submissions.shape[0]),
        ('bad_submission_count', 'Mittekompileeruvaid esitusi', int(students['Bad_submissions'].sum())),
        ('min_grade', 'Minimaalne hinne', float(students['Max_Grade'].min())),
        ('max_grade', 'Maksimaalne hinne', float(students['Max_Grade'].max())),
        ('min_submission_count', 'Vähim arv esitusi õpilase kohta', int(students['Submissions'].min())),
        ('max_submission_count', 'Suurim arv esitusi õpilase kohta', int(students['Submissions'].max())),
        ('first_submission_date', 'Esimene esituse aeg', start_date.strftime('%d/%m/%Y %X')),
        ('last_submission_date', 'Viimane esituse aeg', end_date.strftime('%d/%m/%Y %X'))
    ]

    return general


def point_groups_general():
    point_group_df = get_df('point_group_df')
    point_group_df['Point_Group_Points'] = point_group_df.Point_Group_Points.astype(float)
    point_group_df['Point_Group_Max_Points'] = point_group_df.Point_Group_Max_Points.astype(float)
    point_group_stats = (
        point_group_df.groupby('Point_Group_Name')
        .agg(
            avg_points=('Point_Group_Points', 'mean'),
            max_points=('Point_Group_Max_Points', 'max')  # assuming max is consistent
        )
        .round(2)
    )

    point_group_stats_general = []

    for group, row in point_group_stats.iterrows():
        base_key = group.lower()
        point_group_stats_general.append((f'avg_{base_key}_points', f'Keskmine {base_key}', float(row['avg_points'])))
        point_group_stats_general.append(
            (f'max_{base_key}_points', f'Maksimaalne {base_key}', float(row['max_points'])))

    return point_group_stats_general


def submission_count_timeline() -> alt.Chart:
    submission_df = filter_dataframe(get_df('submission_df'))
    submission_df = submission_df.dropna()
    return alt.Chart(submission_df, name="submission_count_timeline").mark_line().encode(
        alt.X('monthdate(Submission_Time):T', title="Esituste aeg", axis=alt.Axis(format='%d %b')),
        alt.Y('count():Q', title="Esituste arv"),
    ).properties(width=1000).interactive()


def submission_count_heatmap() -> alt.Chart:
    submission_df = filter_dataframe(get_df('submission_df'))
    submission_df = submission_df.dropna()
    return alt.Chart(submission_df, name="submission_count_timeline").mark_rect().encode(
        alt.X('hours(Submission_Time):O', title="Esituste tund"),
        alt.Y('monthdate(Submission_Time):O', title="Esituste päev"),
        alt.Color('count():Q', title="Esituste arv"),
    ).properties(width=700)


def last_grading_point_group_distribution() -> alt.Chart:
    last_point_group_df = filter_dataframe(get_df('last_point_groups_df'))
    last_point_group = last_point_group_df.dropna(
        subset=['Point_Group_Points', 'Point_Group_Max_Points'])
    last_point_group['Point_Group_Points'] = last_point_group.Point_Group_Points.astype(float)
    last_point_group['Point_Group_Max_Points'] = last_point_group['Point_Group_Max_Points'].astype(float)
    last_point_group = last_point_group.drop(columns=['Student_ID', 'Submission_ID', "Submission_Time"])
    point_groups_grouped = last_point_group.groupby('Point_Group_Name').mean()
    point_groups_grouped_indexed = point_groups_grouped.reset_index()

    return alt.Chart(point_groups_grouped_indexed,
                     name="Õpilaste viimase hinde kujunemise jaotuvus punktigruppidena").mark_arc().encode(
        alt.Theta("Point_Group_Points:Q").stack(True),
        alt.Radius("Point_Group_Points").scale(type="sqrt", zero=True, rangeMin=14),
        alt.Color("Point_Group_Name:N", title="Punktigrupid"),
    )


def starting_time_effect_on_point_groups() -> alt.FacetChart:
    points_df = filter_dataframe(get_df('point_group_df'))
    first_submission_time = points_df['Submission_Time'].min()
    last_submission_time = points_df['Submission_Time'].max()

    full_range = (last_submission_time - first_submission_time).total_seconds()

    # Get time from the first submission per submission
    points_df['time_from_start'] = (
            points_df['Submission_Time'] - first_submission_time
    ).dt.total_seconds()

    # Submission time percentiles based on the full submission timeline
    points_df['submission_percentile'] = points_df['time_from_start'] / full_range

    points_df['start_bucket'] = pd.cut(
        points_df['submission_percentile'],
        bins=[0, 1 / 3, 2 / 3, 1],
        labels=['Early', 'Mid', 'Late']
    )

    label_map = {
        'Early': 'Varajane',
        'Mid': 'Keskmine',
        'Late': 'Hiline'
    }

    # Make points float
    points_df['Point_Group_Points'] = points_df.Point_Group_Points.astype(float)

    # Get average scores from point groups
    avg_scores = (
        points_df.groupby(['start_bucket', 'Point_Group_Name'], observed=True)
        .agg({
            'Point_Group_Points': 'mean'
        })
        .reset_index()
    )

    avg_scores['start_label'] = avg_scores['start_bucket'].map(label_map)

    return alt.Chart(avg_scores).mark_bar().encode(
        x=alt.X('start_bucket:N',
                title=None,
                axis=alt.Axis(
                    labelExpr="""
                    datum.value === 'Early' ? 'Varajane' :
                    datum.value === 'Mid' ? 'Keskmine' :
                    datum.value === 'Late' ? 'Hiline' :
                    datum.value
                """
                )
                ),
        y=alt.Y('Point_Group_Points:Q', title='Keskmised punktid'),
        color=alt.Color('start_label:N', title='Algusaja kategooria')
    ).properties(width=200).facet(
        column=alt.Column('Point_Group_Name:N', title='Punktigrupid')
    ).configure_axis(
        gridColor='#4f78d644',  # faint halo blue
        gridDash=[2, 2],
        labelColor='#cfd8dc',
        titleColor='#ffffff'
    )


# Maybe something here?
def submission_count_binned(submission_df: pd.DataFrame) -> alt.Chart:
    submission_df = submission_df.dropna()
    return alt.Chart(submission_df).mark_bar().encode(
        x=alt.X('Submission_Grade:Q', bin=True),
        y='count()'
    ).interactive()
