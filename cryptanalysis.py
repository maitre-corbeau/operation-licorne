#!/usr/bin/env python3

from cypher import decypher
from itertools import product

# frequence des lettres
frequence_theorique = [8.4, 1.06, 3.03, 4.18, 17.26, 1.12, 1.27, 0.92, 7.34, 0.31, 0.05, 6.01, 2.96, 7.13, 5.26, 3.01, 0.99, 6.55, 8.08, 7.07, 5.74, 1.32, 0.04, 0.45, 0.3, 0.12]

theoretical_ci = 0.0778

alphabet="abcdefghijklmnopqrstuvwxyz"

def compute_ci(text):
    text_len = 0
    occurence = []
    for c in alphabet:
        char_count = text.count(c)
        occurence.append(char_count)
        text_len += char_count
    return sum([x * (x - 1) for x in occurence]) / (text_len * (text_len - 1))

def cut_text(text, nb_parts):
    parts = [""] * nb_parts
    ind = 0
    for c in text:
        parts[ind] += c
        ind = (ind + 1)% nb_parts
    return parts

def find_keylength(text, max_length=10):
    prob_key = [1, abs(theoretical_ci - compute_ci(text))]
    for key_len in range(2, max_length):
        diff = 0
        for text_parts in cut_text(text, key_len):
            ci_part = compute_ci(text_parts)
            diff += abs(theoretical_ci - ci_part)
        diff /= key_len
        if diff < prob_key[1]:
            prob_key = [key_len, diff]
    return prob_key[0]

def get_frequency(text):
    frequencies = {}
    total = 0
    for c in alphabet:
        frequencies[c] = 0
    for c in filter(lambda c: c.isalpha(),text):
        frequencies[c] += 1
        total += 1
    total *= .01
    for c in alphabet:
        frequencies[c] /= total
    return list(frequencies.values())

def brute_force(cypher, keylen, threshold=1):
    for possible_key in product(alphabet, repeat=keylen):
        f = get_frequency(decypher(cypher, possible_key))
        d = sum(map(lambda x,y: abs(x-y)/26, f, frequence_theorique))
        if d < threshold:
            print(possible_key)
            return 

def dico_search(cypher, keylen, dico_file, threshold=1):
    with open(dico_file, "r") as dico:
        for key in filter(lambda c: len(c) == keylen, [x.strip("\n").lower() for x in dico.readlines()]):
            f = get_frequency(decypher(cypher, key))
            d = sum(map(lambda x,y: abs(x-y)/26, f, frequence_theorique))
            if d < threshold:
                print(key, d)
