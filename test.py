import sys
from datetime import datetime

from analysis import analyse
from unpacker import unpack

start = datetime.now()

data = unpack()
analyse(data)

exit_message = "Program end."
end = datetime.now()
sys.exit(f"EXIT: {exit_message} Time: {datetime.now()}. Runtime: {(end - start).total_seconds()}s.")
