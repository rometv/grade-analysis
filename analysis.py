""" Main analysis file for creating Altair visualizations. """
import altair as alt
import pandas as pd

from helpers import filter_dataframe
from data_store import get
import numpy as np

"""
Reminder:
    - The submissions dataframe contains processed submission information such as
      `student_id`, `submission_id`, `grade`, `timestamp`, and `runtime`.
    - The point_group dataframe contains group-specific details for each submission,
      including `submission_id`, `group_name`, `points`, `points_max`,
      `weighted_points`, and `weighted_points_max`.
"""


def general_data() -> [str, str, any]:
    submissions = get('submission_df')
    students = submissions.groupby('student_id').agg(
        num_submissions=('submission_id', 'count'),
        max_grade=('grade', 'max'),
        first_submission=('timestamp', 'min'),
        last_submission=('timestamp', 'max')
    ).reset_index()
    start_date = submissions['timestamp'].min()
    end_date = submissions['timestamp'].max()

    general = [
        ('student_count', 'Tudengeid kokku', students.shape[0]),
        ('submissions_count', 'Esitusi kokku', submissions.shape[0]),
        ('underfifty', 'Lõplikke hindeid alla 50%', int(students['max_grade'].le(50).sum())),
        #  ('bad_submission_count', 'Mittekompileeruvaid esitusi', int(students['Bad_submissions'].sum())),
        ('max_grade', 'Maksimaalne hinne', float(students['max_grade'].max())),
        ('min_submission_count', 'Vähim arv esitusi õpilase kohta', int(students['num_submissions'].min())),
        ('max_submission_count', 'Suurim arv esitusi õpilase kohta', int(students['num_submissions'].max())),
        ('first_submission_date', 'Esimene esituse aeg', start_date.strftime('%d/%m/%Y %X')),
        ('last_submission_date', 'Viimane esituse aeg', end_date.strftime('%d/%m/%Y %X'))
    ]

    return general


def submission_count_timeline() -> alt.LayerChart:
    submission_df = filter_dataframe(get('submission_df')).dropna()

    tooltip = [
        alt.Tooltip('monthdate(timestamp):T', title='Kuupäev'),
        alt.Tooltip('count():Q', title='Esituste arv')
    ]

    line = alt.Chart(submission_df).mark_line(point=False).encode(
        x=alt.X('monthdate(timestamp):T', title="Esituste aeg", axis=alt.Axis(format='%d %b')),
        y=alt.Y('count():Q', title="Esituste arv"),
    )

    points = alt.Chart(submission_df).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X('monthdate(timestamp):T'),
        y=alt.Y('count():Q'),
        tooltip=tooltip
    )

    return (line + points).interactive().properties(
        width=1000,
        height=300,
        title={
            "text": ["Esituste ajakava"],
            "subtitle": ["Kujutab esituste arvu muutumist ajas."]
        },
    )


def submission_count_heatmap() -> alt.Chart:
    submission_df = filter_dataframe(get('submission_df'))
    submission_df = submission_df.dropna()
    return alt.Chart(submission_df, name="submission_count_timeline").mark_rect().encode(
        alt.X('hours(timestamp):O', title="Esituste tund"),
        alt.Y('monthdate(timestamp):O', title="Esituste päev"),
        alt.Color('count():Q', title="Esituste arv", scale=alt.Scale(scheme="viridis")),
        tooltip=[
            alt.Tooltip('monthdate(timestamp):T', title="Esituste aeg"),
            alt.Tooltip('hours(timestamp):O', title="Esituste tund"),
            alt.Tooltip('count():Q', title="Esituste arv"),
        ]
    ).properties(width=700, title={
        "text": ["Esituste soojuskaart"],
        "subtitle": ["Visualiseerib esituste sagedust terves esituste ajavahemikus, päeva ja tunni kaupa."]
    })


def last_grading_point_group_time_buckets() -> alt.Chart:
    submissions = filter_dataframe(get('submission_df'))

    last_submissions = (
        submissions.sort_values('timestamp')
        .groupby('student_id')
        .tail(1)
        .copy()
    )

    first = last_submissions['timestamp'].min()
    last = last_submissions['timestamp'].max()
    full_range = (last - first).total_seconds()

    cut_early = first + (last - first) * (1 / 3)
    cut_mid = first + (last - first) * (2 / 3)

    bucket_ranges = {
        'Early': f"{first.strftime('%d/%m/%Y')} – {cut_early.strftime('%d/%m/%Y')}",
        'Mid': f"{cut_early.strftime('%d/%m/%Y')} – {cut_mid.strftime('%d/%m/%Y')}",
        'Late': f"{cut_mid.strftime('%d/%m/%Y')} - {last.strftime('%d/%m/%Y')}",
    }

    last_submissions['time_from_start'] = (
            last_submissions['timestamp'] - first
    ).dt.total_seconds().copy()

    last_submissions['submission_percentile'] = last_submissions['time_from_start'] / full_range

    last_submissions['submission_bucket'] = pd.cut(
        last_submissions['submission_percentile'],
        bins=[0, 1 / 3, 2 / 3, 1],
        labels=['Early', 'Mid', 'Late'],
        include_lowest=True
    )

    last_submissions = last_submissions.dropna(subset=['submission_bucket'])

    label_map = {
        'Late': 'Hiline',
        'Mid': 'Keskmine',
        'Early': 'Varajane',
    }

    last_submissions['bucket_label'] = last_submissions['submission_bucket'].map(
        lambda x: f"{label_map[str(x)]} ({bucket_ranges[str(x)]})"
    )

    bucket_counts = (
        last_submissions
        .groupby('bucket_label', observed=True)
        .agg(student_count=('student_id', 'count'))
        .reset_index()
    )

    return alt.Chart(bucket_counts).mark_arc(innerRadius=20).encode(
        theta=alt.Theta("bucket_label:N", sort=None),
        radius=alt.Radius("student_count:Q", scale=alt.Scale(type="sqrt", rangeMin=20, rangeMax=120)),
        color=alt.Color("bucket_label:N", title="Viimase esituse aeg",
                        legend=alt.Legend(orient="bottom", direction="vertical", labelLimit=300),
                        scale=alt.Scale(scheme="blues", domain=[
                            f"Varajane ({bucket_ranges['Early']})",
                            f"Keskmine ({bucket_ranges['Mid']})",
                            f"Hiline ({bucket_ranges['Late']})"
                        ])),
        tooltip=[
            alt.Tooltip('bucket_label:N', title='Ajavahemik'),
            alt.Tooltip('student_count:Q', title='Õpilaste arv')
        ]
    ).properties(title={
        "text": ["Viimaste esituste ajavahemike jaotus"],
        "subtitle": ["Esituste kogu ajavahemik on jaotatud sektoriteks, kus iga sektor näitab,",
                     "mitu tudengit selles perioodis oma viimase esituse teinud on."]
    })


def starting_time_effect_on_point_groups() -> alt.FacetChart:
    points_df = filter_dataframe(get('point_group_df'))

    first_submission_time = points_df['timestamp'].min()
    last_submission_time = points_df['timestamp'].max()
    full_range = (last_submission_time - first_submission_time).total_seconds()

    cut_early = first_submission_time + (last_submission_time - first_submission_time) * (1 / 3)
    cut_mid = first_submission_time + (last_submission_time - first_submission_time) * (2 / 3)

    bucket_ranges = {
        'Early': f"{first_submission_time.strftime('%d/%m/%Y')} – {cut_early.strftime('%d/%m/%Y')}",
        'Mid': f"{cut_early.strftime('%d/%m/%Y')} – {cut_mid.strftime('%d/%m/%Y')}",
        'Late': f"{cut_mid.strftime('%d/%m/%Y')} – {last_submission_time.strftime('%d/%m/%Y')}",
    }

    points_df['time_from_start'] = (
            points_df['timestamp'] - first_submission_time
    ).dt.total_seconds().copy()

    points_df['submission_percentile'] = points_df['time_from_start'] / full_range

    points_df['start_bucket'] = pd.cut(
        points_df['submission_percentile'],
        bins=[0, 1 / 3, 2 / 3, 1],
        labels=['Early', 'Mid', 'Late'],
        include_lowest=True
    )

    label_map = {
        'Early': 'Varajane',
        'Mid': 'Keskmine',
        'Late': 'Hiline'
    }

    points_df['start_label'] = points_df['start_bucket'].map(
        lambda x: f"{label_map[str(x)]} ({bucket_ranges[str(x)]})"
    )

    avg_scores = (
        points_df.groupby(['start_bucket', 'group_name', 'start_label'], observed=True)
        .agg({
            'points': 'mean',
            'points_max': 'max'
        })
        .reset_index()
    )

    return alt.Chart(avg_scores).mark_bar().encode(
        x=alt.X('start_bucket:N',
                title=None,
                axis=alt.Axis(
                    labelExpr="""
                    datum.value === 'Early' ? 'Varajane' :
                    datum.value === 'Mid' ? 'Keskmine' :
                    datum.value === 'Late' ? 'Hiline' :
                    datum.value
                    """,
                    labelAngle=-45,
                ),
                sort=['Early', 'Mid', 'Late'],
                ),
        y=alt.Y('points:Q', title='Keskmised punktid'),
        color=alt.Color('start_label:N',
                        title='Aegade vahemikud',
                        scale=alt.Scale(
                            scheme="inferno",
                            domain=[
                                f"Varajane ({bucket_ranges['Early']})",
                                f"Keskmine ({bucket_ranges['Mid']})",
                                f"Hiline ({bucket_ranges['Late']})"
                            ]
                        ),
                        legend=alt.Legend(
                            orient="bottom",
                            direction="vertical",
                            labelLimit=1000,
                            columns=1
                        )
                        ),
        tooltip=[
            alt.Tooltip('group_name:N', title='Punktigrupp'),
            alt.Tooltip('start_label:N', title='Esitusaja vahemik'),
            alt.Tooltip('points_max:Q', title='Maksimaalsed punktid', format=".0f"),
            alt.Tooltip('points:Q', title='Keskmised punktid', format=".2f"),
        ]
    ).properties(width=200).facet(
        column=alt.Column('group_name:N', title='Punktigrupid'),
        spacing=5,
        title={
            "text": ["Punktigruppide tulpdiagrammid ajavahemike lõikes"],
            "subtitle": ["Aitab mõista, kuidas ajavahemik on seotud konkreetse punktigrupi keskmise hindega."]
        },
    ).resolve_scale(
        y='shared'
    ).configure_axis(
        gridColor='#4f78d644',
        gridDash=[2, 2],
        labelColor='#cfd8dc',
        titleColor='#ffffff'
    )


def last_grading_point_group_distribution() -> alt.Chart:
    submissions = filter_dataframe(get('submission_df'))
    point_groups = get('point_group_df')

    last_submissions = (
        submissions.sort_values('timestamp')
        .groupby('student_id')
        .tail(1)
        .copy()
    )

    last_point_group_df = pd.merge(
        last_submissions[['student_id', 'submission_id']],
        point_groups,
        on='submission_id'
    )

    last_point_group_df = last_point_group_df.dropna(subset=['points', 'points_max'])
    last_point_group_df['points'] = last_point_group_df['points'].astype(float)
    last_point_group_df['points_max'] = last_point_group_df['points_max'].astype(float)

    avg_grouped = last_point_group_df.groupby('group_name', as_index=False).mean(numeric_only=True)

    return alt.Chart(avg_grouped).mark_arc(innerRadius=20).encode(
        theta=alt.Theta("group_name:N", sort=None),
        radius=alt.Radius("points:Q", scale=alt.Scale(type="sqrt", rangeMin=20, rangeMax=120)),
        color=alt.Color("group_name:N", title="Punktigrupp",
                        legend=alt.Legend(direction="vertical", labelLimit=500),
                        scale=alt.Scale(scheme="greens")),
        tooltip=[
            alt.Tooltip("group_name:N", title="Punktigrupp"),
            alt.Tooltip("points:Q", title="Keskmised punktid", format=".2f"),
            alt.Tooltip("points_max:Q", title="Maksimaalsed punktid", format=".0f"),
        ]
    ).properties(title={
        "text": ["Lõpliku keskmise hinde punktigrupid"],
        "subtitle": ["Lõpliku keskmise hinde kujunemine punktigruppide keskmiste punktide jaotuses.",
                     "Kasutatud on tudengite viimaseid esitusi."]
    })


def grade_improvement() -> alt.LayerChart:
    df = filter_dataframe(get('submission_df')).sort_values(by=['student_id', 'timestamp'])
    df["submission_number"] = df.groupby("student_id").cumcount() + 1
    df = df.drop(columns=["timestamp"])

    all_stats = []
    for num_bins in range(3, 11):
        df_loop = df.copy()
        bin_edges = np.linspace(df_loop["submission_number"].min(), df["submission_number"].max() + 1, num_bins + 1,
                                dtype=int)

        df_loop["bucket"] = pd.cut(df_loop["submission_number"], bins=bin_edges, include_lowest=True)
        df_loop["bucket_str"] = df_loop["bucket"].apply(
            lambda x: f"{max(1, int(x.left))}–{int(x.right - 1)}"
        )

        stats = df_loop.groupby("bucket_str", observed=True).agg(
            q1=("grade", lambda x: x.quantile(0.25)),
            q3=("grade", lambda x: x.quantile(0.75)),
            median=("grade", "median"),
            min_grade=("grade", "min"),
            max_grade=("grade", "max"),
            avg_grade=("grade", "mean"),
            submission_count=("grade", "count"),
            student_count=("student_id", "nunique")
        ).reset_index()
        stats["bin_midpoint"] = bin_edges[:-1] + np.diff(bin_edges) / 2
        stats["bin_count"] = num_bins
        stats["bucket_index"] = range(len(stats))
        all_stats.append(stats)

    full_stats = pd.concat(all_stats, ignore_index=True)

    bin_slider = alt.binding_range(min=3, max=10, step=1, name="Kastide arv ")
    bin_select = alt.selection_single(fields=["bin_count"], bind=bin_slider, value=6)

    x_encoding = alt.X(
        "bucket_str:N",
        title="Esituste arvu vahemik",
        sort=alt.EncodingSortField(field="bucket_index", order="ascending"),
        axis=alt.Axis(labelAngle=-45)
    )

    boxes = alt.Chart(full_stats).transform_filter(bin_select).mark_bar(size=20).encode(
        x=x_encoding,
        y=alt.Y("q1:Q", title="Hinne"),
        y2="q3:Q",
        tooltip=[
            alt.Tooltip("bucket_str:N", title="Esituste vahemik"),
            alt.Tooltip("submission_count:Q", title="Esituste arv"),
            alt.Tooltip("student_count:Q", title="Õpilaste arv"),
            alt.Tooltip("avg_grade:Q", format=".2f", title="Keskmine hinne"),
            alt.Tooltip("median:Q", format=".2f", title="Mediaanhinne"),
            alt.Tooltip("min_grade:Q", format=".2f", title="Minimaalne hinne"),
            alt.Tooltip("max_grade:Q", format=".2f", title="Maksimaalne hinne")
        ]
    )

    whiskers = alt.Chart(full_stats).transform_filter(bin_select).mark_rule(color="white").encode(
        x=x_encoding,
        y="min_grade:Q",
        y2="max_grade:Q"
    )

    ticks = alt.Chart(full_stats).transform_filter(bin_select).mark_tick(color="white", size=20).encode(
        x=x_encoding,
        y="median:Q"
    )

    return (whiskers + boxes + ticks).add_selection(bin_select).properties(
        width=600,
        height=400,
        title={
            "text": ["Esituste vahemike karpdiagramm"],
            "subtitle": [
                "Graafik kujutab hindepiire (miinimum, maksimum, mediaan, keskmine), mis esituste vahemikesse jäävad.",
                "Kastide (karpide) arv muudetav."]
        },
    )


def student_scatter_grade_by_submission_count() -> alt.LayerChart:
    df = filter_dataframe(get('submission_df'))

    student_stats = df.groupby("student_id").agg(
        submission_count=("submission_id", "count"),
        average_grade=("grade", "mean"),
        max_grade=("grade", "max")
    ).reset_index()

    df_long = pd.melt(
        student_stats,
        id_vars=["student_id", "submission_count"],
        value_vars=["average_grade", "max_grade"],
        var_name="grade_type",
        value_name="grade"
    )

    grade_toggle = alt.binding_radio(
        options=["average_grade", "max_grade"],
        labels=["Keskmine hinne", "Maksimaalne hinne"],
        name="Uuritav hinne"
    )

    grade_select = alt.param(
        name="grade_type",
        bind=grade_toggle,
        value="average_grade"
    )

    scatter = alt.Chart(df_long).transform_filter(
        "datum.grade_type === grade_type"
    ).mark_circle(size=60, opacity=0.5).encode(
        x=alt.X("submission_count:Q", title="Esituste arv", scale=alt.Scale(type="log")),
        y=alt.Y("grade:Q", title="Hinne"),
        color=alt.Color("grade:Q", title="Hinde värv", scale=alt.Scale(scheme="blues")),
        tooltip=[
            alt.Tooltip("grade:Q", title="Hinne", format=".2f"),
            alt.Tooltip("submission_count:Q", title="Esituste arv")
        ]
    ).interactive().properties(
        title={
            "text": ['Hinde hajuvusdiagramm regressioonijoonega'],
            "subtitle": ["Kujutab vastavalt uuritava hinde valikule, kus õpilased hinde-esituste arvu skaalal asuvad."]
        }
    )

    trendline = alt.Chart(df_long).transform_filter(
        "datum.grade_type === grade_type"
    ).transform_regression(
        "submission_count", "grade"
    ).mark_line(color="white").encode(
        x="submission_count:Q",
        y="grade:Q"
    )

    return (scatter + trendline).add_params(grade_select)
