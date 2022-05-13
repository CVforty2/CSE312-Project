from typing import *

OP_MASK: int = 0xf
PAYLOAD_MASK: int = 0x7f 
# a helper module to parse bytes

def _OPCODE(byte: bytes) -> int:
    return int.from_bytes(byte, 'big') & OP_MASK

# gets the payload
def _PAYLOAD(byte: bytes) -> int:
    return int.from_bytes(byte, 'big') & PAYLOAD_MASK

# gets the extended payload
def _EXTPAYLOAD(double_bytes: bytes):
    return int.from_bytes(double_bytes, 'big')

# gets the double extended payload
def _EXTEXTPAYLOAD(max_bytes: bytes):
    return int.from_bytes(max_bytes, 'big')