import os

def get_lines(num):
    with open(os.path.join(os.getcwd(), "data", "advent{}.txt".format(num))) as f:
        return f.read().splitlines()
