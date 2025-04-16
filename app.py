import os
import shutil

from flask import Flask, render_template, jsonify, request, redirect, url_for, current_app

from analysis import general_data
from chart_api import SubmissionChartApi, SubmissionHeatMapApi, GradingDistributionApi, StartingTimeEffectOnPointGroups
from data_frames import get_dataframes
from data_store import load_data, get_df
from unpacker import unpack

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["zipfile"]

        if not file or not file.filename.endswith(".zip"):
            return "Please upload a valid zip file", 400

        zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(zip_path)

        data_object = unpack(zip_path)
        students, submissions, point_groups, last_point_groups = get_dataframes(data_object)

        load_data(students, submissions, point_groups, last_point_groups, zip_path)

        return redirect(url_for("index"))

    return render_template("upload.html")


@app.route('/api/general', methods=['GET'])
def get_general_data():
    return jsonify(general_data())


app.add_url_rule(
    "/api/submissions",
    view_func=SubmissionChartApi.as_view("submission_chart")
)
app.add_url_rule(
    "/api/submission_heatmap",
    view_func=SubmissionHeatMapApi.as_view("submission_heatmap")
)
app.add_url_rule(
    "/api/grading_distribution",
    view_func=GradingDistributionApi.as_view("grading_distribution")
)
app.add_url_rule(
    "/api/starting_time_effect_on_grading",
    view_func=StartingTimeEffectOnPointGroups.as_view("starting_time_effect_on_grading")
)


@app.route('/api/testing', methods=['GET'])
def get_testing():
    # chart = testing(student_df, submission_df, point_group_df, last_point_groups_df)
    return {}


@app.route('/')
def index():
    if get_df('student_df') is None:
        return redirect(url_for('upload'))
    else:
        return render_template('dashboard.html')


app.static_folder = 'static'

shutil.rmtree(UPLOAD_FOLDER)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
