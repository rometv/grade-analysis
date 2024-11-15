import hashlib
import re
from datetime import datetime
from zipfile import ZipFile

from data_classes import Student, Submission, PointGroup, Data, grade_in_context


def generate_hash(name):
    # TODO: Better hashing - mix up the moodle id?
    name_to_id = {}
    if name in name_to_id:
        return name_to_id[name]

    enc_name = name.encode('UTF-8')
    hash_name = hashlib.sha256(enc_name).hexdigest()
    std_id = hash_name[:8]
    name_to_id[name] = std_id
    return std_id


def parse(moodle_file: ZipFile) -> Data:
    data: Data = Data([])
    prev_id = None
    student = None
    submissions = 0
    files = moodle_file.namelist()

    for i in range(0, len(files) + 1):
        is_last = i == len(files)
        file = files[i] if not is_last else ''

        if re.search(r'^((?!ceg|java|Report|class).)*$', file) or is_last:
            # Student submissions folder
            names_list = file.split(" ")
            names_list.reverse()

            # Get hashed id
            current_id = generate_hash(names_list[1]) if not is_last else ''

            # Switch student
            if prev_id != current_id or is_last:
                if prev_id is not None:
                    student.set_no_of_submissions(submissions)
                    if is_last:
                        break
                    submissions = 0
                prev_id = current_id

            student = Student(current_id)

        # Read all submitted .java files
        if re.search(r'java|class', file):
            submissions += 1

        # Execution file for parsing out results
        if re.search(r'.ceg/execution.txt', file):
            execution_file = str(moodle_file.open(file, 'r').read().decode('UTF-8'))

            # Fun ops
            time = file.split('/')[1].removesuffix('.ceg')
            date_time = datetime.strptime(time, '%Y-%m-%d-%H-%M-%S')
            grade = re.search(r'Grade :=>> (\d+)', execution_file)

            # Check for point groups
            reg_point_groups = re.findall(r'(?<=Point groups:).*', execution_file, re.DOTALL)
            point_groups: list[PointGroup] = []
            if len(reg_point_groups) > 0:
                if reg_point_groups[0]:
                    groups = re.findall(r'\[(.*?)]:(.*?\))', reg_point_groups[0])
                    for j in groups:
                        task_name = j[0].strip()
                        points_all = re.findall(r'\d*\.*\d+', j[1])

                        point_groups.append(PointGroup(task_name, points_all[0], points_all[1]))

                    ungrouped = re.findall(r'<ungrouped>:(.*?\))', reg_point_groups[0])

                    # Point groups might be ungrouped, so check for that
                    if ungrouped:
                        ungrouped_points = re.findall(r'\d*\.*\d+', ungrouped[0])
                        point_groups.append(PointGroup('Ungrouped', ungrouped_points[2], ungrouped_points[3]))

                if grade is not None:
                    grade = float(grade.group(0).split()[-1]) / 100
                else:
                    grade = 0

                # Adding data to our result Submission object and add it to the student at hand
                student.add_submission(Submission(date_time, grade_in_context(grade), point_groups))

        # Check if student id has been added
        student_ids = {student.id for student in data.get_students()}
        if prev_id not in student_ids:
            data.add_student(student)

    return data
