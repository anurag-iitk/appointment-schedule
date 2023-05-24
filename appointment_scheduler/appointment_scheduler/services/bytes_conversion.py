import logging
logger = logging.getLogger()


def to_bytes32(s):
    """ This function converts a string to bytes of size 32. It truncates in case bytes size is greater than 32"""
    if not isinstance(s,str):
        if s.decode().rstrip('\x00') == "":
            return None
    b = s.encode()
    if (len(b) > 32):
        return b[:32]
    elif (len(b) < 32):
        return b.ljust(32)
    else:
        return b


def from_bytes32(b):
    if not b:
        return None
    if isinstance(b,str):
        return b
    if len(b)==64: #temp fix and should be removed
        return b.hex()
    if b.decode().rstrip('\x00')=="":
        return None
    # else:
    #     print(b)
    #     return b.decode().rstrip(" ")
    try:
        return b.decode().rstrip(" ")
    except UnicodeDecodeError as e:
        logger.debug("error in bytes conversion, trying as hexadecimal")
        return b.hex().rstrip("x\00")
