# general functions and common patterns 
import ctypes
from numpy import arange
from copy import copy, deepcopy
# flatten nested arrays
flatten = lambda t: [item for sublist in t for item in sublist]


select = lambda array, item: [i[item] for i in array if item in i.keys()][0]

make_integer_safe = lambda i: i - (i-ctypes.c_uint(-1).value)


def merge_attributes(x ,y):
    xcopy = deepcopy(x)
    ycopy = deepcopy(y)
    for nkey, nvalue in ycopy.items():
        if nkey in xcopy: 
            if isinstance(nvalue, dict):
                for key, val in nvalue.items():
                    xcopy[nkey][key] = val
            else:
                xcopy[nkey] = nvalue
    return xcopy

