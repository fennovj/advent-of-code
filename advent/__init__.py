import os
import numpy as np

def get_lines(num, ext='txt'):
    with open(os.path.join(os.getcwd(), "data", "advent{}.{}".format(num, ext))) as f:
        return f.read().splitlines()

def get_char_grid(num, ext="csv"):
    with open(os.path.join(os.getcwd(), "data", "advent{}.{}".format(num, ext))) as f:
        data = f.read().splitlines()
    return np.array([[c for c in line] for line in data])
