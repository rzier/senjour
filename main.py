import socket
from enum import Enum, auto
import numpy as np
import binascii


LISTEN_PORT = 9000
LISTEN_INTERFACE = "0.0.0.0"
BUFFER_SIZE = 1024


sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind((LISTEN_INTERFACE, LISTEN_PORT))

def fetch(buffer):
    for x in buffer:
        yield x



class STATE(Enum):
    STARTED = auto()
    TAGGING = auto()
    SCANNING = auto()
    DATA = auto()

tag = ""
k = 0
val = []
state = STATE.STARTED
pstate = state
vindex = 0

def consume(fetcher):
    global tag, k, state, pstate, val, vindex
    if state == STATE.STARTED:
        tag = ""
        k = 0
        val = []
        vindex = 0
        while next(fetcher) != ord('/'): pass
        state = STATE.TAGGING
    if state == STATE.TAGGING:
        while (ch := next(fetcher)) != 0:
            tag += chr(ch)
        state = STATE.SCANNING
    if state == STATE.SCANNING:
        while next(fetcher) != ord(','): pass
        while next(fetcher) == ord('f'):
            k += 1
        next(fetcher)
        state = STATE.DATA
    if state == STATE.DATA:
        for vindex in range(vindex, (k * 4 + (k - 1))):
            l = vindex
            if l > 0 and (l % 4) == ((l // 4) - 1):
                next(fetcher)
            else:
                val += [ next(fetcher) ]
    return (tag, k, val)


while True:
    buffer = sock.recv(BUFFER_SIZE)
    fetcher = fetch(buffer)
    try:
        tag, k, v = consume(fetcher)
        u = np.frombuffer(np.array(v[::-1], dtype=np.uint8).tobytes(), dtype=np.float32)
        print(tag, k, u)
        state = STATE.STARTED
    except StopIteration as s:
        continue
