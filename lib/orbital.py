
from math import sqrt

# orbital maths

def derive_semi_axis(e,major):
  """Inputs: eccentricity, semi-major axis; Outputs: semi-minor axis"""
  return major*(math.sqrt(1-e**2))

