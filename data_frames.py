import pandas as pd

from data_classes import Data
from data_classes import Student


def get_dataframes(data: Data) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    student_data = []
    submission_data = []
    point_group_data = []
    last_submission_data = []

    # Iterate through each student
    for student in data.get_students():
        student_id = student.id
        no_of_submissions = student.get_no_of_submissions()
        max_grade = student.get_grade()
        time_taken = student.get_time_taken()
        non_compilable_submissions = student.get_no_of_non_compilable_submissions()
        average_time = student.get_average_time_between_submission()
        last_submission = student.get_last_submission()
        first_submission = student.get_first_submission()

        # Append student data to student_data list
        student_data.append({
            "Student_ID": student_id,
            "Submissions": no_of_submissions,
            "Bad_submissions": non_compilable_submissions,
            "Max_Grade": max_grade,
            "Time_taken": time_taken,
            "Avg_time_between_submissions": average_time,
            "First_submission_date": first_submission.time if first_submission else 0,
            "Last_submission_date": last_submission.time if last_submission else 0
        })

        if last_submission:
            for point in last_submission.point_groups:
                last_submission_data.append({
                    "Student_ID": student_id,
                    "Submission_ID": point.submission_id,
                    "Submission_Time": last_submission.time if last_submission else 0,
                    "Point_Group_Name": point.name,
                    "Point_Group_Points": point.points,
                    "Point_Group_Max_Points": point.max_points,
                })

        # Iterate through each submission of the student
        for submission in student.get_submissions():
            submission_time = submission.time
            submission_grade = submission.grade
            submission_id = submission.submission_id

            # Append submission data to submission_data list
            submission_data.append({
                "Submission_ID": submission_id,
                "Student_ID": student_id,
                "Submission_Time": submission_time,
                "Submission_Grade": submission_grade
            })

            # Iterate through each point group of the submission
            for point_group in submission.point_groups:
                point_group_name = point_group.name
                point_group_points: float = point_group.points
                point_group_max_points: float = point_group.max_points

                # Append point group data to point_group_data list
                point_group_data.append({
                    "Submission_ID": submission_id,
                    "Student_ID": student_id,
                    "Submission_Time": submission_time,
                    "Point_Group_Name": point_group_name,
                    "Point_Group_Points": point_group_points,
                    "Point_Group_Max_Points": point_group_max_points
                })

    return pd.DataFrame(student_data), pd.DataFrame(submission_data), pd.DataFrame(point_group_data), pd.DataFrame(last_submission_data)
