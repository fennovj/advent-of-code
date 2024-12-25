import numpy as np
from typing import Any
from math import prod

def np_where_as_tuple(data, char):
    matches = np.where(data == char)
    return [(matches[0][i], matches[1][i]) for i in range(len(matches[0]))]

def tadd2(x: tuple[Any, Any], y: tuple[Any, Any]):
    return (x[0] + y[0], x[1] + y[1])

def tsub2(x: tuple[Any, Any], y: tuple[Any, Any]):
    return (x[0] - y[0], x[1] - y[1])

def tmul2(c: Any, x: tuple[Any, Any]):
    return (c * x[0], c * x[1])

def chinese_remainder(a, m):
    # Given a_i, m_i, where all m_i are coprime:
    # Calculate n such that n_i % m_i = a_i
    sum = 0
    prodm = prod(m)
    for n_i, a_i in zip(m, a):
        p = prodm // n_i
        sum += a_i * pow(p, n_i) * p
    return sum % prodm