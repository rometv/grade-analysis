import sys

from analysis import analyse
from unpacker import unpack


def load_all(result_file):
    try:
        return unpack(result_file)
    except FileNotFoundError:
        file_error = f'Filename "{result_file}" was not found!'
        sys.exit(f'EXIT: {file_error}')


results = ""
subs, users, per_student, aio = load_all(results)
analyse(subs, users, per_student, aio)
