from zipfile import ZipFile

from data_classes import Data
from parser import parse

def unpack(path: str) -> Data:
    with ZipFile(path, 'r') as moodle_file:
        return parse(moodle_file)