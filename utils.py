import hashlib
from datetime import datetime

import pandas as pd
import altair as alt
from scipy.stats import stats

from tabulate import tabulate as tab

root_dir = 'charts/'


def save(chart: alt.Chart):
    time = datetime.now().strftime("%Y-%d-%m-%H-%M-%S")
    print(time)
    chart.save(fp=f'{root_dir}{chart.name}.json')


def table(df: pd.DataFrame):
    print(tab(df, headers='keys', tablefmt='pretty'))


def pearson(list1, list2):
    return stats.pearsonr(list1, list2)


def grade_in_context(grade: float) -> int:
    return round((grade * 10000) / 80)


def is_dir(path):
    return path.endswith('/')


def generate_hash(name):
    # TODO: "Better hashing" - mix up the moodle id?
    name_to_id = {}
    if name in name_to_id:
        return name_to_id[name]
    enc_name = name.encode('UTF-8')
    hash_name = hashlib.sha256(enc_name).hexdigest()
    std_id = hash_name[:8]
    name_to_id[name] = std_id
    return std_id
