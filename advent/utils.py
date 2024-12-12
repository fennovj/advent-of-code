import numpy as np
from typing import Any

def np_where_as_tuple(data, char):
    matches = np.where(data == char)
    return [(matches[0][i], matches[1][i]) for i in range(len(matches[0]))]

def tadd2(x: tuple[Any, Any], y: tuple[Any, Any]):
    return (x[0] + y[0], x[1] + y[1])
