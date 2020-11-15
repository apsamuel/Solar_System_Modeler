import os, sys
sys.path.extend([os.path.join('.', 'lib')])
from math import sqrt
from blender import frame, frames, normalized_frame




def derive_semiminor_axis(planet):
  """Inputs: Planet; Outputs: semi-minor axis"""
  semiMajorAxis = planet.semimajorAxis 
  e = planet.eccentricity
  return (semiMajorAxis*(sqrt(1-e**2)))

def get_z_euler_rot_function(planet):
  """Inputs: Planet; Outputs: driver expression for Z-Euler rotation"""
  return f"(360/{planet.sideralRotation})*frame()"

def get_x_loc_function(planet, var):
  """Inputs: Planet; Outputs: driver expression for a planets X location"""
  return f"({var}*(cos(normalized_frame())))+0"    

def get_y_loc_function(planet,var):
  """Inputs: Planet; Outputs: driver expression for planets Y location"""
  return f"({var}*(sin(normalized_frame())))+0"



