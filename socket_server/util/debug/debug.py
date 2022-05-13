import os
from sys import stdout, stderr

def debug_print(string: str) -> None:
    if not os.getenv('production'):
        print(string)
        stdout.flush()
        stderr.flush()