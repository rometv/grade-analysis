import datetime


class PointGroup:
    """
        A particular point group with its name and grading.

        Parameters:
            submission_id (str): The id of the submission.
            name (str): Name of the group.
            points (float): The amount of points user got in that particular point group.
            max_points (float): The maximum amount of points possible in that particular point group.
        """

    def __init__(self, submission_id: str, name: str, points: float, max_points: float):
        self.submission_id = submission_id
        self.name: str = name
        self.points: float = points
        self.max_points: float = max_points

    def __str__(self):
        return f'PointGroup: {self.name} - {self.points}/{self.max_points}'


class Submission:
    """
        A particular submission with its name, grading and point group.

        Parameters:
            submission_id (str): The id of the submission.
            time (datetime.datetime): Date and time of submission.
            point_groups (List[PointGroup]): List of point-group objects.
            grade (float): Grade of the submission.
    """

    def __init__(self, submission_id: str, time: datetime, grade: float, point_groups: list[PointGroup]):
        self.submission_id: str = submission_id
        self.time: datetime = time
        self.grade: float = grade
        self.point_groups: list[PointGroup] = point_groups

    def __str__(self):
        return f"Submission: Time - {self.time}, Grade - {self.grade}"


class Student:
    """
    A particular student with its name, grading and point group.

    Parameters:
        hashed_id (str): Unique student id.
    """

    def __init__(self, hashed_id: str):
        self.id: str = hashed_id
        self.submissions: list[Submission] = []
        self.no_of_submissions: int = 0
        self.max_grade: float = 0

    def __str__(self):
        return (
            f'Student: Hashed Id - {self.id}, № Of Submissions - {self.no_of_submissions}, Submissions - '
            f'{self.get_submissions()},'
            f' Final grade - {self.get_grade()}'
        )

    def get_grade(self):
        grades = [float(submission.grade) for submission in self.submissions]
        return max(grades) if grades else 0

    def add_submission(self, submission: Submission):
        self.submissions.append(submission)

    def get_submissions(self):
        sorted_submissions = sorted(self.submissions, key=lambda submission: submission.time)
        return sorted_submissions

    def set_no_of_submissions(self, no_of_submissions: int):
        self.no_of_submissions = no_of_submissions

    def get_no_of_submissions(self):
        return self.no_of_submissions

    def get_no_of_non_compilable_submissions(self):
        non_compilable_submissions = self.get_no_of_submissions() - len(self.submissions)
        return non_compilable_submissions if non_compilable_submissions >= 0 else self.get_no_of_submissions()

    def get_time_taken(self):
        submissions = self.get_submissions()
        if len(submissions) > 1:
            first_submission_time = submissions[0].time
            last_submission_time = submissions[-1].time

            timedelta = (last_submission_time - first_submission_time)

            return timedelta.total_seconds() \
                if (last_submission_time > first_submission_time) else 0

        return 0

    def get_average_time_between_submission(self):
        submissions = self.get_submissions()
        if len(submissions) >= 2:
            time_diffs = [submissions[i].time - submissions[i - 1].time for i in range(1, len(submissions))]
            total_time_diff = sum(time_diffs, datetime.timedelta(0)) / len(time_diffs)
            return total_time_diff.total_seconds()

        return 0

    def get_first_submission(self) -> Submission | None:
        if len(self.get_submissions()) > 0:
            return self.get_submissions()[0]

    def get_last_submission(self) -> Submission | None:
        if len(self.get_submissions()) > 0:
            return self.get_submissions()[-1]


class Data:
    """
    A class to hold the data for all students and their submissions.
    Parameters:
        students (List[Student]): A list of students.
    """

    def __init__(self, students):
        self.students: list[Student] = []

    def __str__(self):
        return f'Students: {len(self.students)}'

    def add_student(self, student: Student):
        self.students.append(student)

    def get_students(self):
        return self.students
