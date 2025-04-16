import hashlib
import sys
from datetime import datetime

from unpacker import unpack

start = datetime.now()
#
# data = unpack()
# test_analyse(data)

exit_message = "Program end."

hunja = "ewgfjnbefrgjkbnerfbljnuikwrgikljubndefrgi"

parool = "kuionmustnäitaust"





end = datetime.now()
sys.exit(f"EXIT: {exit_message} Time: {datetime.now()}. Runtime: {(end - start).total_seconds()}s.")
