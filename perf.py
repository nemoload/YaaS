import os
import signal
import time
from merge import fib

s = time.time()

def int_handler(signum_frame,frame):
    e = time.time()
    print("\n")
    print(e-s)
    exit(0)
signal.signal(signal.SIGINT, int_handler)


fib(50)

e = time.time()
print(e-s)