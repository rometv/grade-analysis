from flask.views import MethodView

from analysis import submission_count_timeline, submission_count_heatmap, last_grading_point_group_distribution, \
    starting_time_effect_on_point_groups, grade_improvement, student_scatter_grade_by_submission_count, \
    last_grading_point_group_time_buckets


class BaseChartApi(MethodView):
    chart_funct = None

    def get(self):
        chart = self.chart_funct()
        return chart.to_json()


class SubmissionChartApi(BaseChartApi):
    chart_funct = staticmethod(submission_count_timeline)


class SubmissionHeatMapApi(BaseChartApi):
    chart_funct = staticmethod(submission_count_heatmap)


class LastGradePointGroupPieChartApi(BaseChartApi):
    chart_funct = staticmethod(last_grading_point_group_distribution)


class LastGradeTimeRangePieChartApi(BaseChartApi):
    chart_funct = staticmethod(last_grading_point_group_time_buckets)


class StartingTimeEffectOnPointGroups(BaseChartApi):
    chart_funct = staticmethod(starting_time_effect_on_point_groups)


class GradeImprovement(BaseChartApi):
    chart_funct = staticmethod(grade_improvement)


class GradeBySubmissionCountScatter(BaseChartApi):
    chart_funct = staticmethod(student_scatter_grade_by_submission_count)
