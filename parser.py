import hashlib
import re

from datetime import datetime
from random import sample
from zipfile import ZipFile

from data_classes import Student, Submission, PointGroup, Data
from utils import is_dir, generate_hash, grade_in_context

java_or_class = re.compile(r'java|class')
execution_txt = re.compile(r'.ceg/execution.txt')
re_grade = re.compile(r'Grade :=>> (\d+)')
re_point_groups = re.compile(r'(?<=Point groups:).*', re.DOTALL)
re_groups_old = re.compile(r'\[(.*?)]:(.*?\))')
re_groups = re.compile(r'^(.+?):\s*(.+)$', re.MULTILINE)
re_points_all = re.compile(r'\d*\.*\d+')
re_ungrouped = re.compile(r'<ungrouped>:(.*?\))')


def parse(moodle_file: ZipFile) -> Data:
    data: Data = Data([])
    prev_id = None
    current_student = None
    submissions = 0
    files = moodle_file.namelist()

    for i in range(0, len(files) + 1):
        is_last = i == len(files)
        file = files[i] if not is_last else ''

        if is_dir(file):
            names_list = file.split(" ")
            names_list.reverse()
            current_id = generate_hash(names_list[1]) if not is_last else ''

            if prev_id != current_id and current_id != '':
                if prev_id is not None:
                    current_student.set_no_of_submissions(submissions)
                    if is_last:
                        break
                    submissions = 0
                prev_id = current_id

            current_student = Student(current_id)

        else:
            if re.search(java_or_class, file):
                submissions += 1

            if re.search(execution_txt, file):
                execution_file = str(moodle_file.open(file, 'r').read().decode('UTF-8'))

                # Get time and grade from execution file
                time = file.split('/')[1].removesuffix('.ceg')
                date_time = datetime.strptime(time, '%Y-%m-%d-%H-%M-%S')
                grade = re.search(re_grade, execution_file)

                # Check for point groups
                reg_point_groups = re.findall(re_point_groups, execution_file)
                point_groups: list[PointGroup] = []
                submission_id = ''.join(sample(hashlib.sha256(current_student.id.encode()).hexdigest(), 8))
                if len(reg_point_groups) > 0:
                    if reg_point_groups[0]:
                        reg_point_group = reg_point_groups[0].split('<|--')[0]
                        groups = re.findall(re_groups, reg_point_group)

                        if len(groups) == 0:
                            groups = re.findall(re_groups_old, reg_point_groups[0])

                        for j in groups:
                            task_name = j[0].strip()
                            points_all = re.findall(re_points_all, j[1])

                            if len(points_all) > 0: point_groups.append(
                                PointGroup(submission_id, task_name, points_all[0], points_all[1]))

                        ungrouped = re.findall(re_ungrouped, reg_point_groups[0])

                        # Point groups might be ungrouped, so check for that (if you want)
                        if ungrouped:
                            ungrouped_points = re.findall(re_points_all, ungrouped[0])
                            point_groups.append(
                                PointGroup(submission_id, 'Ungrouped', ungrouped_points[2], ungrouped_points[3]))

                    if grade is not None:
                        grade_as_float: float = float(grade.group(0).split()[-1]) / 100
                    else:
                        grade_as_float: float = 0

                    # Adding data to result Submission object and append it to the student at hand
                    submission = Submission(submission_id, date_time, grade_in_context(grade_as_float), point_groups)
                    current_student.add_submission(submission)

        # Check if student id has been added
        student_ids = {student.id for student in data.get_students()}
        if prev_id not in student_ids:
            data.add_student(current_student)

    return data
