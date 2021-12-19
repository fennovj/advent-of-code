import os
import numpy as np

def get_lines(num, ext='txt', map_fn=None):
    with open(os.path.join(os.getcwd(), "data", "advent{}.{}".format(num, ext))) as f:
        data = f.read().splitlines()
    return [map_fn(c) for c in data] if map_fn else data

def get_lines_doublenewline(num, ext='txt'):
    with open(os.path.join(os.getcwd(), "data", "advent{}.{}".format(num, ext))) as f:
        data = f.read().split("\n\n")
    return [c.splitlines() for c in data]

def get_char_grid(num, ext="csv"):
    with open(os.path.join(os.getcwd(), "data", "advent{}.{}".format(num, ext))) as f:
        data = f.read().splitlines()
    return np.array([[c for c in line] for line in data])
