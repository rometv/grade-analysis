"""Common utility functions shared across the project. Documentation provided by AI assistant."""

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
    """
    Generates a unique hash-based identifier for a given name.

    This function generates an identifier based on the SHA-256 hash of the provided student Moodle ID.
    The identifier is created by encoding the input name to UTF-8, hashing it using SHA-256, and
    truncating the resulting hash to the first 8 characters. A caching mechanism ensures that
    repeated calls with the same name return the same identifier.

    Args:
        name (str): The name for which to generate a unique identifier.

    Returns:
        str: An 8-character unique identifier for the given name.
    """
    name_to_id = {}
    if name in name_to_id:
        return name_to_id[name]
    enc_name = name.encode('UTF-8')
    hash_name = hashlib.sha256(enc_name).hexdigest()
    std_id = hash_name[:8]
    name_to_id[name] = std_id
    return std_id


def chunkify(lst, n):
    """
    Splits a list into smaller lists of a specified size and yields them.

    This function divides the input list into chunks of the given size `n` and
    yields these chunks one at a time. Each chunk will contain elements from the
    input list, and the last chunk may contain fewer elements if the total number
    of elements is not evenly divisible by `n`.

    Args:
        lst: List to be divided into chunks.
        n: Integer specifying the size of each chunk.

    Yields:
        Sub-lists of the original list, each of size `n`, except possibly the last
        sub-list, which may have fewer elements.
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
