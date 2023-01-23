import os

# Set exit codes in a platform-independent way
try:
    EXIT_OK = os.EX_OK
except AttributeError:
    EXIT_OK = 0
try:
    EXIT_DATAERR = os.EX_DATAERR
except AttributeError:
    EXIT_DATAERR = 65
try:
    EXIT_USAGE = os.EX_USAGE
except AttributeError:
    EXIT_USAGE = 64
