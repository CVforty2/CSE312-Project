import os
from typing import *
from util.debug.debug import debug_print

def compare_files(filename1: str, filename2: str) -> None:
    if not os.getenv('production'):
        debug_print(f"------------------------------- IMAGE INFO FOR {filename1} -------------------------------")
        with open(f"sample_page/image/{filename1}", "rb") as firstImage,\
            open(f"sample_page/uimage/{filename2}", "rb") as secondImage:
            firstImageBytes: bytes = firstImage.read()
            secondImageBytes: bytes = secondImage.read()
            __diff(firstImageBytes, secondImageBytes)
            if len(firstImageBytes) != len(secondImageBytes):
                debug_print("Lengths of the images do not match!")
                debug_print(f"Length of sample_page/image/{filename1}: {len(firstImageBytes)}")
                debug_print(f"Length of sample_page/image/uimage/{filename2}: {len(secondImageBytes)}")
                if len(firstImageBytes) > len(secondImageBytes):
                    debug_print(f"sample_page/image/{filename1} is larger than sample_page/image/uimage/{filename2}")
                    debug_print(f"Difference: {len(firstImageBytes) - len(secondImageBytes)} bytes")
                else:
                    debug_print(f"sample_page/image/{filename1} is smaller than sample_page/image/uimage/{filename2}")
                    debug_print(f"Difference: {len(secondImageBytes) - len(firstImageBytes)} bytes")
            else:
                debug_print("Lengths of the files are the same!")
                debug_print(f"Length of sample_page/image/{filename1}: {len(firstImageBytes)}")
                debug_print(f"Length of sample_page/image/uimage/{filename2}: {len(secondImageBytes)}")
        debug_print("------------------------------- DONE -------------------------------")


def __diff(filebytes1: bytes, filebytes2: bytes) -> None:
    for byte_index in range(min(len(filebytes1), len(filebytes2))):
        if filebytes1[byte_index] != filebytes2[byte_index]:
            debug_print(f"Difference spotted at byte {byte_index}:")
            debug_print(f"First file: {filebytes1[byte_index]}, Second file: {filebytes2[byte_index]}")