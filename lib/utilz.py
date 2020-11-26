# general functions and common patterns 
import ctypes
from numpy import arange
# flatten nested arrays
flatten = lambda t: [item for sublist in t for item in sublist]


select = lambda array, item: [i[item] for i in array if item in i.keys()][0]

make_integer_safe = lambda i: i - (i-ctypes.c_uint(-1).value)

