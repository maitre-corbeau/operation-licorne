#!/usr/bin/env python3

import sys
import os
from unidecode import unidecode

def shift_char(c, shift):
    return chr(97 + (ord(c) - 97 + shift) % 26) 

def shift_text(text, stream):
    shifted = ""
    ind = 0
    stream_len = len(stream)

    for c in text:
        shifted += shift_char(c, stream[ind])
        ind = (ind + 1) % stream_len

    return shifted


def cypher(clear, key):
    stream = [ord(x) - 97 for x in key]
    return shift_text(clear, stream)

def decypher(cypher, key):
    stream = [-1 * (ord(x) - 97) for x in key]
    return shift_text(cypher, stream)

def cypher_file(in_file, out_file, key):
    with open(in_file, "r") as f:
        clear = f.read()

    cyphered = cypher(filter_alpha(clear), key)

    with open(out_file, "w") as f:
        print(cyphered, file=f)

def decypher_file(in_file, out_file, key):
    with open(in_file, "r") as f:
        cypher = f.read()

    clear = decypher(filter_alpha(cypher), key)

    with open(out_file, "w") as f:
        print(clear, file=f)

def filter_alpha(text):
    utext = unidecode(text, "utf-8")
    return "".join(filter(lambda c: c.isalpha(), unidecode(utext).lower()))
        

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("cypher.py input_file output_file key", file=sys.stderr)
        sys.exit(1)

    fn = sys.argv[1]
    newbook = sys.argv[2]
    key = sys.argv[3]

    with open(fn, "r") as f:
        clear = f.read()

    cyphered = cypher(filter_alpha(clear), key)

    with open(newbook, "w") as f:
        print(cyphered, file=f)
