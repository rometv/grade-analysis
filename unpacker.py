import hashlib
import re
from datetime import datetime
from zipfile import ZipFile

name_to_id = {}


def generate_hash(name):
    if name in name_to_id:
        return name_to_id[name]

    enc_name = name.encode('UTF-8')
    hash_name = hashlib.sha256(enc_name).hexdigest()
    std_id = hash_name[:8]
    name_to_id[name] = std_id
    return std_id


def unpack(file):
    with ZipFile(file, 'r') as moodle_file:
        report = moodle_file.open("Report.txt").read()
        data_per_student = {}
        all_data = []
        no_of_users = None
        no_of_subs = None

        try:
            no_of_users = int(re.split(r'Number of users: (\d+)', str(report))[1])
            no_of_subs = int(re.split(r'Number of submissions: (\d+)', str(report))[1])
        except:
            print('Failed')

        prev_id = None
        for file in moodle_file.infolist():
            if re.search(r'.ceg/execution.txt', file.filename):
                current_id = generate_hash(re.split(r'\d', file.filename.split("/")[0])[0].strip())
                if prev_id != current_id:

                    if prev_id is not None:
                        data_per_student[prev_id].sort()
                    prev_id = current_id

                execution_file = str(moodle_file.open(file.filename).read())

                # Fun ops
                time = file.filename.split('/')[1].removesuffix('.ceg')
                date_time = datetime.strptime(time, '%Y-%m-%d-%H-%M-%S')
                grade = re.search(r'Grade :=>> (\d+)', execution_file)

                # Check for point groups
                point_groups = re.findall(r'(?<=Point groups:).*', execution_file)[0]
                if point_groups:
                    point_groups = re.findall(r'\[(.*?)\]:(.*?\))', point_groups)
                    points = {}
                    tasks = {}
                    for i in point_groups:
                        task_name = i[0]
                        points_all = re.findall(r'(?:\d*\.*\d+)', i[1])

                        points[task_name] = points_all[0], points_all[1]
                        tasks[task_name] = points_all[2], points_all[3]

                if grade is not None:
                    grade = float(grade.group(0).split()[-1]) / 100
                else:
                    grade = 0

                # Check if student id has been added
                if prev_id not in data_per_student:
                    data_per_student[prev_id] = []

                # Adding data to our result file(s)
                data_per_student[prev_id].append([date_time, grade, points, tasks])
                all_data.append([prev_id, date_time, grade, points, tasks])

    return no_of_subs, no_of_users, data_per_student, all_data
