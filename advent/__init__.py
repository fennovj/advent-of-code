import os
import numpy as np

def get_lines(num: int, ext: str='txt', map_fn=None):
    with open(os.path.join(os.getcwd(), "data", "advent{}.{}".format(num, ext))) as f:
        data = f.read().splitlines()
    return [map_fn(c) for c in data] if map_fn else data

def get_lines_doublenewline(num: int, ext: str='txt'):
    with open(os.path.join(os.getcwd(), "data", "advent{}.{}".format(num, ext))) as f:
        data = f.read().split("\n\n")
    return [c.splitlines() for c in data]

def get_char_grid(num: int, ext: str="csv", map_fn=None):
    with open(os.path.join(os.getcwd(), "data", "advent{}.{}".format(num, ext))) as f:
        data = f.read().splitlines()
    data = [[c for c in line] for line in data]
    if map_fn: data = [[map_fn(c) for c in line] for line in data]
    return np.array(data)

def get_intcode(num: int, ext: str='txt'):
    # reads input that is a single line of ints, e.g. "1,2,3"
    return list(map(int, get_lines(num, ext)[0].split(',')))