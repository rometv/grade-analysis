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
            no_of_users = int(re.split("Number of users: (\d+)", str(report))[1])
            no_of_subs = int(re.split("Number of submissions: (\d+)", str(report))[1])
        except:
            print("Failed")

        prev_id = None
        for file in moodle_file.infolist():
            if re.search(".ceg/execution.txt", file.filename):
                current_id = generate_hash(re.split("\d", file.filename.split("/")[0])[0].strip())
                if prev_id != current_id:

                    if prev_id is not None:
                        data_per_student[prev_id].sort()
                    prev_id = current_id

                # Fun ops
                time = file.filename.split("/")[1].removesuffix(".ceg")
                date_time = datetime.strptime(time, '%Y-%m-%d-%H-%M-%S')
                grade = re.search("Grade :=>> (\d+)", str(moodle_file.open(file.filename).read()))

                if grade is not None:
                    grade = float(grade.group(0).split()[-1]) / 100
                else:
                    grade = 0

                # Check if student id has been added
                if prev_id not in data_per_student:
                    data_per_student[prev_id] = []

                # Adding data to our result file(s)
                data_per_student[prev_id].append([date_time, grade])
                all_data.append([prev_id, date_time, grade])

    return no_of_subs, no_of_users, data_per_student, all_data
