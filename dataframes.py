import pandas as pd

from data_classes import Data


def get_dataframes(data: Data) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    student_data = []
    submission_data = []
    point_group_data = []

    # Iterate through each student
    for student in data.get_students():
        student_id = student.id
        no_of_submissions = student.get_no_of_submissions()
        max_grade = student.get_grade()
        time_taken = student.get_time_taken()
        non_compilable_submissions = student.get_no_of_non_compilable_submissions()
        average_time = student.get_average_time_between_submission()
        last_submission = student.get_last_submission()

        # Append student data to student_data list
        student_data.append({
            "Id": student_id,
            "Submissions": no_of_submissions,
            "Bad submissions": non_compilable_submissions,
            "Max_Grade": max_grade,
            "Time taken": time_taken,
            "Avg time between submissions": average_time,
            "Last submission date": last_submission.time if last_submission else 0
        })

        # Iterate through each submission of the student
        for submission in student.get_submissions():
            submission_time = submission.time
            submission_grade = submission.grade

            # Append submission data to submission_data list
            submission_data.append({
                "Student_ID": student_id,
                "Submission_Time": submission_time,
                "Submission_Grade": submission_grade
            })

            # Iterate through each point group of the submission
            for point_group in submission.point_groups:
                point_group_name = point_group.name
                point_group_points = point_group.points
                point_group_max_points = point_group.max_points

                # Append point group data to point_group_data list
                point_group_data.append({
                    "Student_ID": student_id,
                    "Submission_Time": submission_time,
                    "Point_Group_Name": point_group_name,
                    "Point_Group_Points": point_group_points,
                    "Point_Group_Max_Points": point_group_max_points
                })

    return pd.DataFrame(student_data), pd.DataFrame(submission_data), pd.DataFrame(point_group_data)
