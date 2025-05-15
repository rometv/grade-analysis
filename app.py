""" Flask application for grade analysis. AI generated function documentation."""
import os
import shutil

from flask import Flask, render_template, jsonify, request, redirect, url_for

from analysis import general_data
from chart_api import SubmissionChartApi, SubmissionHeatMapApi, StartingTimeEffectOnPointGroups, \
    GradeImprovement, GradeBySubmissionCountScatter, LastGradePointGroupPieChartApi, LastGradeTimeRangePieChartApi
from data_store import load_data, get
from parse_homework import parse_homework

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/api/hw_name", methods=["GET"])
def hw_name():
    homework_name = get('current_zip_name')
    if homework_name is None:
        return {'error': 'Homework name not found'}, 404
    else:
        return homework_name, 200


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Handles the file upload functionality for a web application. Allows users to upload
    a ZIP file containing homework submissions. It validates the file type, processes the contents,
    and updates the application's configuration with relevant data.

    Returns:
        A redirect to the main page if the upload and processing are successful.
        A rendered HTML template if the request method is GET.
        An error message with status code 400 if an invalid file is uploaded.
    """
    if request.method == "POST":
        file = request.files["zipfile"]

        if not file or not file.filename.endswith(".zip"):
            return "Please upload a valid zip file", 400

        zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(zip_path)

        try:
            submissions_df, point_groups_df = parse_homework(zip_path)
            load_data(submissions_df, point_groups_df, file.filename)
        except Exception as e:
            return {
                "message": "Error processing zip file",
                "error": str(e),
            }, 400

        return redirect(url_for("index"))

    return render_template("upload.html")


@app.route('/api/general', methods=['GET'])
def get_general_data():
    """
    Handles the API endpoint for fetching general data.

    This function serves the '/api/general' endpoint and handles GET requests.
    It fetches data using the `general_data` function and returns it as a JSON
    response.

    Returns:
        Response: A Flask Response object containing the JSON representation
            of the general data.
    """
    try:
        return general_data()
    except Exception as e:
        return {
            "message": "Failed to fetch general data",
            "error": str(e),
        }, 404


@app.route('/api/date_range', methods=['GET'])
def get_date_range():
    """
    Handles the retrieval of a date range based on query parameters provided
    in an HTTP GET request. The function checks the presence of 'start_date'
    and 'end_date' query parameters, formats their response as strings, and
    returns a JSON response. If either of the parameters is missing, it returns
    an error response.

    Returns:
        Response: A JSON response containing the formatted date range as strings
        ("start_date" and "end_date") if both parameters are provided. If either
        parameter is missing, returns a JSON error response with a 404 status
        code.

    Raises:
        KeyError: Raised if query parameter keys ('start_date', 'end_date') are
        missing in the request.
    """
    start = get('start_date')
    end = get('end_date')

    if start is None or end is None:
        return {"error": "No date range available"}, 404

    return jsonify({
        "start_date": start.strftime("%d/%m/%Y"),
        "end_date": end.strftime("%d/%m/%Y")
    })


@app.route('/api/purge', methods=['POST'])
def purge_uploads():
    """
    Clears all uploaded files and resets related application configurations.

    This function handles the clearing of all uploaded files from the upload folder
    on the server and resets several application-level configurations. It ensures
    that the upload directory is re-created after the deletion. If an error occurs
    during the process, the function returns an error message.

    Returns:
        tuple: A tuple containing a dictionary with a success message or error
        details, and an HTTP status code (200 for success, 500 for failure).
    """
    try:
        shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        app.config['student_df'] = None
        app.config['submission_df'] = None
        app.config['point_group_df'] = None
        app.config['last_point_groups_df'] = None
        app.config['zip_filename'] = None

        return {"message": "Uploads cleared successfully!"}, 200
    except Exception as e:
        return {"message": "Failed to clear uploads.", "error": str(e)}, 500


@app.route('/')
def index():
    """
    Handles the default route of the application and redirects the user based on the
    presence of specific data stored in memory.

    Redirects to the 'upload' page if necessary data is missing; otherwise, serves
    the main dashboard page for the user.

    Returns:
        Response: A redirection to the 'upload' route if required resources are not
        available, or a rendered HTML template for the dashboard.
    """
    if get('submission_df') is None and get('point_group_df') is None:
        return redirect(url_for('upload'))
    else:
        return render_template('dashboard.html')


"""
Chart rules

Chart API routes:
    - /api/submissions
    - /api/submission_heatmap
    - /api/grading_distribution
    - /api/starting_time_effect_on_grading
    - /api/grade_improvement
    
Chart functions:
    - submission_count_timeline
    - submission_count_heatmap
    - last_grading_point_group_distribution
    - starting_time_effect_on_point_groups
    - grade_improvement_distribution
"""
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
    view_func=LastGradePointGroupPieChartApi.as_view("grading_distribution")
)

app.add_url_rule(
    "/api/last_grade_time_pie_chart",
    view_func=LastGradeTimeRangePieChartApi.as_view("last_grade_time_pie_chart")
)

app.add_url_rule(
    "/api/starting_time_effect_on_grading",
    view_func=StartingTimeEffectOnPointGroups.as_view("starting_time_effect_on_grading")
)

app.add_url_rule(
    "/api/grade_by_submission_count_scatter",
    view_func=GradeBySubmissionCountScatter.as_view("grade_by_submission_count_scatter"),
)

app.add_url_rule("/api/grade_improvement", view_func=GradeImprovement.as_view("grade_improvement"))

app.static_folder = 'static'

shutil.rmtree(UPLOAD_FOLDER)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
