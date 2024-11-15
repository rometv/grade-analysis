from zipfile import ZipFile

from data_classes import Data
from parser import parse


def unpack(url: str = "") -> Data:
    # TODO: Get data from the webz?
    # response = requests.get(url)
    # filename = 'latest.zip'
    # with open(filename, 'wb') as f:
    #     f.write(response.content)
    #     print(f'File with the name "{filename}" was written!')
    root_dir = 'packed_homework_files/Algoritmid ja andmestruktuurid/'
    name = "4. Kodutöö esitamine"

    with ZipFile(f'{root_dir}{name}.zip', 'r') as moodle_file:
        return parse(moodle_file)
