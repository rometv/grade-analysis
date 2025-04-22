from flask.views import MethodView

from analysis import submission_count_timeline, submission_count_heatmap, last_grading_point_group_distribution, \
    starting_time_effect_on_point_groups, grade_improvement


class BaseChartApi(MethodView):
    chart_funct = None

    def get(self):
        chart = self.chart_funct()
        return chart.to_json()


class SubmissionChartApi(BaseChartApi):
    chart_funct = staticmethod(submission_count_timeline)


class SubmissionHeatMapApi(BaseChartApi):
    chart_funct = staticmethod(submission_count_heatmap)


class GradingDistributionApi(BaseChartApi):
    chart_funct = staticmethod(last_grading_point_group_distribution)


class StartingTimeEffectOnPointGroups(BaseChartApi):
    chart_funct = staticmethod(starting_time_effect_on_point_groups)

class GradeImprovement(BaseChartApi):
    chart_funct = staticmethod(grade_improvement)